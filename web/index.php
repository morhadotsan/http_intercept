<?php require_once __DIR__."/lib/db.php"; ?>
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>http_intercept</title>
	<link rel="stylesheet" href="public/style.css">
</head>
<body>
	<header>
		<h1>http_intercept</h1>
		<p>Scan a URL and grade its security headers.</p>
	</header>

	<section class="scan-box">
		<form id="scan-form">
			<input type="text" id="url-input" placeholder="https://example.com" required>
			<button type="submit">Scan</button>
		</form>
		<div id="status"></div>
	</section>

	<section id="result" class="hidden">
		<div class="grade-box">
			<div class="grade" id="grade"></div>
			<div class="score" id="score"></div>
			<div class="meta" id="meta"></div>
		</div>
		<table id="tests-table">
			<thead><tr><th>Header</th><th>Status</th><th>Value</th><th>Points</th><th>Notes</th></tr></thead>
			<tbody></tbody>
		</table>
	</section>

	<section class="history">
		<h2>Recent scans</h2>
		<div class="compare-bar">
			<button id="compare-btn" disabled>Compare selected (0)</button>
			<span class="hint">Pick two rows to compare.</span>
		</div>
		<table id="history-table">
			<thead><tr><th></th><th>URL</th><th>Last scan</th><th>Grade</th><th>Score</th><th>Scans</th></tr></thead>
			<tbody></tbody>
		</table>
	</section>

	<section id="compare-result" class="hidden">
		<h2>Comparison</h2>
		<div id="compare-summary"></div>
		<table id="compare-table">
			<thead><tr><th>Header</th><th>A</th><th>B</th><th>Changed</th></tr></thead>
			<tbody></tbody>
		</table>
	</section>

	<script src="public/main.js"></script>
</body>
</html>
