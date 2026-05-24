const $ = (id) => document.getElementById(id);
const selected = new Set();

document.addEventListener("DOMContentLoaded", () => {
	$("scan-form").addEventListener("submit", onScan);
	$("compare-btn").addEventListener("click", onCompare);
	loadHistory();
});

async function onScan(e){
	e.preventDefault();
	const url = $("url-input").value.trim();
	if(!url) return;
	$("status").textContent = "Scanning...";
	$("result").classList.add("hidden");

	try {
		const res = await fetch("api/scan.php", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ url })
		});
		const data = await res.json();
		$("status").textContent = "";
		renderResult(data.result);
		loadHistory();
	} catch(err) {
		$("status").textContent = "Scan failed: "+err.message;
	}
}

function renderResult(r){
	$("result").classList.remove("hidden");
	if(r.status !== "success"){
		$("grade").textContent = "?";
		$("grade").className = "grade";
		$("grade").removeAttribute("data-grade");
		$("score").textContent = "";
		$("meta").textContent = "Error: "+(r.error_message||"unknown");
		$("tests-table").querySelector("tbody").innerHTML = "";
		return;
	}
	$("grade").textContent = r.grade;
	$("grade").className = "grade";
	$("grade").setAttribute("data-grade", r.grade);
	$("score").textContent = r.score;
	$("meta").textContent = `${r.final_url} • HTTP ${r.status_code}`;

	const tbody = $("tests-table").querySelector("tbody");
	tbody.innerHTML = "";
	for(const t of r.tests){
		const tr = document.createElement("tr");
		tr.innerHTML = `
			<td>${escapeHtml(t.header_name)}</td>
			<td class="status-${t.status}">${t.status}</td>
			<td class="value">${escapeHtml(t.header_value || "—")}</td>
			<td>${t.points}</td>
			<td>${escapeHtml(t.message || "")}</td>
		`;
		tbody.appendChild(tr);
	}
}

async function loadHistory(){
	const res = await fetch("api/history.php");
	const data = await res.json();
	const tbody = $("history-table").querySelector("tbody");
	tbody.innerHTML = "";
	for(const u of (data.urls || [])){
		const tr = document.createElement("tr");
		tr.innerHTML = `
			<td><input type="checkbox" data-url="${escapeAttr(u.url)}"></td>
			<td>${escapeHtml(u.url)}</td>
			<td>${escapeHtml(u.last_scanned_at)}</td>
			<td>${escapeHtml(u.latest_grade || "—")}</td>
			<td>${u.latest_score ?? "—"}</td>
			<td>${u.scan_count}</td>
		`;
		tbody.appendChild(tr);
	}
	tbody.querySelectorAll("input[type=checkbox]").forEach(cb => {
		cb.addEventListener("change", onPick);
	});
}

async function onPick(e){
	const url = e.target.dataset.url;
	if(e.target.checked){
		selected.add(url);
		if(selected.size > 2){
			e.target.checked = false;
			selected.delete(url);
		}
	}else{
		selected.delete(url);
	}
	const btn = $("compare-btn");
	btn.textContent = `Compare selected (${selected.size})`;
	btn.disabled = selected.size !== 2;
}

async function onCompare(){
	const urls = [...selected];
	const [a, b] = await Promise.all(urls.map(u => fetch("api/history.php?url="+encodeURIComponent(u)).then(r=>r.json())));
	const idA = a.scans?.[0]?.scan_id;
	const idB = b.scans?.[0]?.scan_id;
	if(!idA || !idB){
		alert("One of the URLs has no scans yet.");
		return;
	}
	const res = await fetch(`api/compare.php?a=${idA}&b=${idB}`);
	const data = await res.json();
	renderCompare(data);
}

function renderCompare(data){
	$("compare-result").classList.remove("hidden");
	$("compare-summary").innerHTML = `
		<div><strong>A:</strong> ${escapeHtml(data.a.url)} — ${data.a.grade || "?"} (${data.a.score ?? "—"}) at ${data.a.scanned_at}</div>
		<div><strong>B:</strong> ${escapeHtml(data.b.url)} — ${data.b.grade || "?"} (${data.b.score ?? "—"}) at ${data.b.scanned_at}</div>
	`;
	const tbody = $("compare-table").querySelector("tbody");
	tbody.innerHTML = "";
	for(const row of data.diff){
		const tr = document.createElement("tr");
		if(row.changed) tr.className = "changed";
		tr.innerHTML = `
			<td>${escapeHtml(row.header_name)}</td>
			<td class="value">${cellFor(row.a)}</td>
			<td class="value">${cellFor(row.b)}</td>
			<td>${row.changed ? "yes" : ""}</td>
		`;
		tbody.appendChild(tr);
	}
}

function cellFor(t){
	if(!t) return "<em>—</em>";
	return `<span class="status-${t.status}">${t.status}</span> · ${escapeHtml(t.header_value||"")} <small>(${t.points})</small>`;
}

function escapeHtml(s){
	return String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]));
}
function escapeAttr(s){ return escapeHtml(s); }
