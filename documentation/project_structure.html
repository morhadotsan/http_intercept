<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>http_intercept &mdash; Project Structure &amp; Flow</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="style.css">
</head>
<body>

<header class="doc-header">
	<h1>http_intercept</h1>
	<p class="subtitle">Project Structure, Architecture &amp; End-to-End Flow Documentation</p>
	<div class="doc-meta">
		<span><strong>Type:</strong> Security-header scanner (self-hosted Mozilla Observatory clone)</span>
		<span><strong>Stack:</strong> PHP + Python (Flask) + SQLite</span>
		<span><strong>Platform:</strong> XAMPP on Windows</span>
	</div>
</header>

<!-- ============================================================
     TABLE OF CONTENTS
     ============================================================ -->
<nav class="toc">
	<h2>Contents</h2>
	<ol>
		<li><a href="#overview">Project Overview</a></li>
		<li><a href="#stack">Technology Stack</a></li>
		<li><a href="#architecture">High-Level Architecture</a></li>
		<li><a href="#file-structure">Project File Structure</a></li>
		<li><a href="#flow">End-to-End Scan Flow</a></li>
		<li><a href="#analyzer">Python Analyzer Component</a></li>
		<li><a href="#web">PHP Web Layer Component</a></li>
		<li><a href="#frontend">Frontend Component</a></li>
		<li><a href="#database">Database Design</a></li>
		<li><a href="#rules">Security Rules &mdash; Per-Header Detail</a></li>
		<li><a href="#scoring">Scoring &amp; Grading System</a></li>
		<li><a href="#api">HTTP API Endpoints</a></li>
		<li><a href="#history-compare">History &amp; Compare Flows</a></li>
		<li><a href="#setup">Setup &amp; Run Instructions</a></li>
		<li><a href="#extending">Extending the Project</a></li>
	</ol>
</nav>

<!-- ============================================================ -->
<section id="overview">
	<h2>1. Project Overview</h2>
	<p>
		<strong>http_intercept</strong> is a security tool that scans a target website&rsquo;s HTTP response, extracts the
		response headers, and grades how well the server is configured against a curated catalogue of security-header
		best practices. It is a <em>self-hosted clone</em> of
		<a href="https://developer.mozilla.org/en-US/observatory">Mozilla Observatory</a>.
	</p>

	<h4>Core Capabilities</h4>
	<ul>
		<li><strong>Scan</strong> &mdash; submit a URL, fetch its headers, and check each against a security rule.</li>
		<li><strong>Grade</strong> &mdash; convert rule outcomes into a numeric score and a letter grade (A+ &rarr; F).</li>
		<li><strong>Persist</strong> &mdash; every scan, with its raw headers, per-rule outcomes, redirect chain and grade, is stored in SQLite.</li>
		<li><strong>History</strong> &mdash; list all previously-scanned URLs with their latest grade.</li>
		<li><strong>Compare</strong> &mdash; diff the latest scans of any two URLs, header by header.</li>
	</ul>

	<h4>Why two languages?</h4>
	<p>
		The project deliberately separates the <em>analyzer</em> from the <em>web layer</em>:
	</p>
	<ul>
		<li>The <strong>Python analyzer</strong> handles the technical work &mdash; HTTP requests, header parsing, rule
			evaluation, HTML/Set-Cookie inspection. Python&rsquo;s <code>requests</code> library makes this trivial and
			the rule engine is easy to extend.</li>
		<li>The <strong>PHP web layer</strong> handles the user-facing concerns &mdash; UI rendering, REST endpoints,
			database persistence. PHP fits naturally on XAMPP and ships with everything needed.</li>
	</ul>
	<p>
		The two layers talk to each other over a small JSON-over-HTTP interface, so either could be swapped or scaled
		independently.
	</p>
</section>

<!-- ============================================================ -->
<section id="stack">
	<h2>2. Technology Stack</h2>
	<table>
		<thead>
			<tr><th>Layer</th><th>Technology</th><th>Purpose</th><th>Key files</th></tr>
		</thead>
		<tbody>
			<tr>
				<td>Analyzer</td>
				<td>Python 3.9+ with <code>Flask 3.0.3</code> and <code>requests 2.32.3</code></td>
				<td>Performs the outbound HTTP fetch and evaluates security headers via pluggable rule modules.</td>
				<td><code>analyzer/app.py</code>, <code>analyzer/scoring.py</code>, <code>analyzer/rules/*.py</code></td>
			</tr>
			<tr>
				<td>Web API</td>
				<td>PHP 8.x (PDO, cURL)</td>
				<td>REST endpoints consumed by the browser; talks to the analyzer; writes to SQLite.</td>
				<td><code>web/api/scan.php</code>, <code>web/api/history.php</code>, <code>web/api/compare.php</code></td>
			</tr>
			<tr>
				<td>Web UI</td>
				<td>HTML5 + CSS3 + Vanilla JavaScript (Fetch API)</td>
				<td>Single-page interface for scanning, browsing history, and comparing scans.</td>
				<td><code>web/index.php</code>, <code>web/public/main.js</code>, <code>web/public/style.css</code></td>
			</tr>
			<tr>
				<td>Persistence</td>
				<td>SQLite 3 (via PHP&rsquo;s <code>pdo_sqlite</code>)</td>
				<td>Stores URLs, scans, and per-test results. File-based; no separate database server.</td>
				<td><code>web/lib/db.php</code>, <code>web/lib/http_intercept_db.sqlite</code></td>
			</tr>
			<tr>
				<td>Hosting</td>
				<td>XAMPP (Apache + PHP) on Windows</td>
				<td>Serves the <code>web/</code> directory at <code>http://localhost/http_intercept/web/</code>.</td>
				<td>n/a (system service)</td>
			</tr>
		</tbody>
	</table>

	<h4>Python modules in use</h4>
	<ul>
		<li><code>flask</code> &mdash; the analyzer is a tiny Flask app with two routes: <code>POST /scan</code> and <code>GET /health</code>.</li>
		<li><code>requests</code> &mdash; performs the outbound HTTP GET, follows redirects, and exposes the redirect chain.</li>
		<li><code>urllib.parse</code> (stdlib) &mdash; used in <code>https_redirect</code> and <code>subresource_integrity</code> to extract hostnames.</li>
		<li><code>re</code> (stdlib) &mdash; used in <code>subresource_integrity</code> to find <code>&lt;script&gt;</code> tags in HTML bodies.</li>
	</ul>

	<h4>PHP extensions in use</h4>
	<ul>
		<li><code>pdo_sqlite</code> &mdash; database access in <code>web/lib/db.php</code>.</li>
		<li><code>curl</code> &mdash; HTTP client in <code>web/lib/analyzer_client.php</code> that posts to the Python analyzer.</li>
		<li><code>filter</code> (built-in) &mdash; URL sanitisation in <code>web/lib/sanitize.php</code>.</li>
	</ul>
</section>

<!-- ============================================================ -->
<section id="architecture">
	<h2>3. High-Level Architecture</h2>
	<p>
		Three independent processes co-operate. The browser talks only to PHP; PHP talks to the analyzer; the analyzer
		talks to the public internet. SQLite is written exclusively by the PHP layer.
	</p>

	<div class="diagram">
		<div class="flow-row">
			<div class="flow-box ext">Browser<span class="sub">Fetch API / HTML</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box php">PHP Web Layer<span class="sub">Apache &middot; XAMPP</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box python">Python Analyzer<span class="sub">Flask &middot; port 5000</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box ext">Target Website<span class="sub">arbitrary URL</span></div>
		</div>
		<span class="flow-arrow down">&darr;</span>
		<div class="flow-row">
			<div class="flow-box db">SQLite<span class="sub">http_intercept_db.sqlite</span></div>
		</div>
		<div class="flow-caption">PHP persists every scan; the analyzer is stateless.</div>
	</div>

	<h4>Process responsibilities</h4>
	<table>
		<thead>
			<tr><th>Process</th><th>Listens on</th><th>Responsibilities</th></tr>
		</thead>
		<tbody>
			<tr>
				<td>Apache (XAMPP)</td>
				<td><code>http://localhost/http_intercept/web/</code></td>
				<td>Serves <code>index.php</code>, static assets, and the three API endpoints. Forwards scan requests to Flask, writes to SQLite.</td>
			</tr>
			<tr>
				<td>Flask analyzer</td>
				<td><code>http://127.0.0.1:5000</code></td>
				<td>Receives <code>POST /scan</code> from PHP, fetches the target URL, runs every rule, returns JSON. No database access.</td>
			</tr>
			<tr>
				<td>SQLite file</td>
				<td>filesystem only</td>
				<td>Three tables (<code>urls</code>, <code>scans</code>, <code>scan_tests</code>). FK enforced at connection time via <code>PRAGMA foreign_keys = ON</code>.</td>
			</tr>
		</tbody>
	</table>

	<div class="callout note">
		<strong>Why isolate the analyzer behind PHP?</strong>
		Two reasons. First, the browser cannot directly fetch arbitrary cross-origin URLs and read response headers,
		so the work must happen server-side. Second, separating the analyzer means a future deployment could put it on
		a different host (configurable via the <code>ANALYZER_URL</code> environment variable read by
		<code>web/lib/analyzer_client.php</code>).
	</div>
</section>

<!-- ============================================================ -->
<section id="file-structure">
	<h2>4. Project File Structure</h2>
	<p>The repository is organised by language layer. Everything that runs in Python lives under <code>analyzer/</code>,
	everything that runs in PHP/Browser lives under <code>web/</code>, and human-readable documentation lives under
	<code>documentation/</code>.</p>

<pre class="tree"><span class="dir">http_intercept/</span>
&#9500;&#9472;&#9472; <span class="dir">analyzer/</span>                        <span class="note"># Python (Flask) &mdash; runs as separate process</span>
&#9474;   &#9500;&#9472;&#9472; <span class="file">app.py</span>                      <span class="note"># Flask app: POST /scan, GET /health, the fetch() helper</span>
&#9474;   &#9500;&#9472;&#9472; <span class="file">scoring.py</span>                  <span class="note"># grade() + score_results() &mdash; converts point sums to letter</span>
&#9474;   &#9500;&#9472;&#9472; <span class="file">requirements.txt</span>            <span class="note"># Flask==3.0.3, requests==2.32.3</span>
&#9474;   &#9500;&#9472;&#9472; <span class="dir">rules/</span>                      <span class="note"># one module per security header</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">__init__.py</span>          <span class="note"># exports ALL_RULES list (registers every rule.check)</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">csp.py</span>               <span class="note"># Content-Security-Policy</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">hsts.py</span>              <span class="note"># Strict-Transport-Security</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">cors.py</span>              <span class="note"># Access-Control-Allow-Origin / Allow-Credentials</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">corp.py</span>              <span class="note"># Cross-Origin-Resource-Policy</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">https_redirect.py</span>    <span class="note"># http:// &rarr; https:// redirect health</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">referrer_policy.py</span>   <span class="note"># Referrer-Policy</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">set_cookie.py</span>        <span class="note"># Secure / HttpOnly / SameSite cookie flags</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">subresource_integrity.py</span> <span class="note"># external &lt;script integrity=&hellip;&gt; checks</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">x_content_type_options.py</span> <span class="note"># nosniff</span>
&#9474;   &#9474;   &#9492;&#9472;&#9472; <span class="file">x_frame_options.py</span>   <span class="note"># DENY / SAMEORIGIN / CSP frame-ancestors</span>
&#9474;   &#9492;&#9472;&#9472; <span class="dir">venv/</span>                       <span class="note"># local Python virtualenv (created by user, gitignored)</span>
&#9500;&#9472;&#9472; <span class="dir">web/</span>                             <span class="note"># PHP layer (UI + API) &mdash; served by XAMPP Apache</span>
&#9474;   &#9500;&#9472;&#9472; <span class="file">index.php</span>                   <span class="note"># single-page UI markup; pulls in style.css + main.js</span>
&#9474;   &#9500;&#9472;&#9472; <span class="dir">api/</span>                        <span class="note"># JSON endpoints consumed by main.js</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">scan.php</span>               <span class="note"># POST: trigger a scan and persist results</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">history.php</span>            <span class="note"># GET: list all URLs OR all scans for one URL</span>
&#9474;   &#9474;   &#9492;&#9472;&#9472; <span class="file">compare.php</span>            <span class="note"># GET: diff two scan_ids and return changed rows</span>
&#9474;   &#9500;&#9472;&#9472; <span class="dir">lib/</span>                        <span class="note"># server-side helpers (canonical location for DB code)</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">db.php</span>                 <span class="note"># PDO connection + createTables() schema bootstrap</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">analyzer_client.php</span>    <span class="note"># analyzer_url() + analyzer_scan() &mdash; cURL POST to Flask</span>
&#9474;   &#9474;   &#9500;&#9472;&#9472; <span class="file">sanitize.php</span>           <span class="note"># clean_url(), host_of(), clean_int()</span>
&#9474;   &#9474;   &#9492;&#9472;&#9472; <span class="file">http_intercept_db.sqlite</span> <span class="note"># the SQLite database file (auto-created)</span>
&#9474;   &#9492;&#9472;&#9472; <span class="dir">public/</span>                     <span class="note"># browser-served static assets</span>
&#9474;       &#9500;&#9472;&#9472; <span class="file">main.js</span>                <span class="note"># UI controller: onScan / loadHistory / onCompare</span>
&#9474;       &#9492;&#9472;&#9472; <span class="file">style.css</span>              <span class="note"># app theme (dark)</span>
&#9500;&#9472;&#9472; <span class="dir">documentation/</span>                   <span class="note"># this report</span>
&#9474;   &#9500;&#9472;&#9472; <span class="file">project_structure.html</span>      <span class="note"># this document</span>
&#9474;   &#9492;&#9472;&#9472; <span class="file">style.css</span>                   <span class="note"># documentation stylesheet (light/print)</span>
&#9500;&#9472;&#9472; <span class="file">README.md</span>                        <span class="note"># short project description</span>
&#9500;&#9472;&#9472; <span class="file">STEPS.md</span>                         <span class="note"># operator&rsquo;s setup &amp; usage guide</span>
&#9500;&#9472;&#9472; <span class="file">CLAUDE.md</span>                        <span class="note"># architectural notes</span>
&#9492;&#9472;&#9472; <span class="file">.gitignore</span>
</pre>
</section>

<!-- ============================================================ -->
<section id="flow">
	<h2>5. End-to-End Scan Flow</h2>
	<p>The most important user journey is &ldquo;type a URL, get a grade&rdquo;. The diagram below traces the lifecycle of a
	single scan request from the moment the user clicks <strong>Scan</strong>.</p>

	<div class="diagram">
		<div class="flow-row">
			<div class="flow-box ext">1. User<span class="sub">submits URL</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box ext">2. main.js<span class="sub">onScan(e)</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box php">3. web/api/scan.php<span class="sub">POST handler</span></div>
		</div>
		<span class="flow-arrow down">&darr;</span>
		<div class="flow-row">
			<div class="flow-box php">4. clean_url()<span class="sub">sanitize.php</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box php">5. analyzer_scan()<span class="sub">analyzer_client.php (cURL)</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box python">6. Flask /scan<span class="sub">app.py</span></div>
		</div>
		<span class="flow-arrow down">&darr;</span>
		<div class="flow-row">
			<div class="flow-box python">7. fetch()<span class="sub">requests.get(url)</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box ext">8. Target<span class="sub">HTTP response</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box python">9. ALL_RULES loop<span class="sub">10 rule.check() calls</span></div>
		</div>
		<span class="flow-arrow down">&darr;</span>
		<div class="flow-row">
			<div class="flow-box python">10. score_results()<span class="sub">scoring.py</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box python">11. jsonify response<span class="sub">grade + tests</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box php">12. scan.php upserts</div>
		</div>
		<span class="flow-arrow down">&darr;</span>
		<div class="flow-row">
			<div class="flow-box db">13. INSERT into urls / scans / scan_tests</div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box ext">14. renderResult()<span class="sub">main.js</span></div>
		</div>
		<div class="flow-caption">14 steps, three processes, one round trip per scan.</div>
	</div>

	<h3>5.1 Step-by-step narrative</h3>
	<ol>
		<li><strong>Submit</strong> &mdash; user types a URL into <code>#url-input</code> and clicks <em>Scan</em>.</li>
		<li><strong>onScan(e)</strong> in <code>web/public/main.js</code> intercepts the form submit, shows
			&ldquo;Scanning&hellip;&rdquo; in <code>#status</code>, and posts JSON to <code>api/scan.php</code>.</li>
		<li><strong>scan.php</strong> reads the JSON body, falls back to <code>$_POST</code> / <code>$_GET</code> for
			flexibility, then calls <code>clean_url()</code>.</li>
		<li><strong>clean_url()</strong> in <code>sanitize.php</code> trims input, prefixes <code>http://</code> if no
			scheme is present, runs <code>FILTER_SANITIZE_URL</code> / <code>FILTER_VALIDATE_URL</code>, and rejects
			anything without a hostname.</li>
		<li><strong>analyzer_scan(url)</strong> in <code>analyzer_client.php</code> resolves the analyzer base URL (from
			<code>ANALYZER_URL</code> env var, default <code>http://127.0.0.1:5000</code>) and uses cURL to POST
			<code>{ "url": &hellip; }</code> with a 30-second timeout.</li>
		<li><strong>Flask</strong> receives the request at <code>/scan</code> in <code>analyzer/app.py</code>, parses the
			JSON body, ensures the URL has a scheme, and dispatches to <code>fetch()</code>.</li>
		<li><strong>fetch(url)</strong> performs <code>requests.get(&hellip;, timeout=10, allow_redirects=True)</code>. It
			captures: HTTP status, the final URL after redirects, the redirect chain, all response headers, all
			<code>Set-Cookie</code> values (using <code>r.raw.headers.get_all</code> to preserve multiples), the content
			type, and &mdash; if HTML &mdash; the response body.</li>
		<li><strong>Target server</strong> returns the response.</li>
		<li><strong>Rule loop</strong> &mdash; <code>app.py</code> builds a <code>context</code> dict and iterates
			<code>ALL_RULES</code> from <code>analyzer/rules/__init__.py</code>, calling each module&rsquo;s
			<code>check(headers, context)</code>. Every rule returns the same shape:
			<code>{header_name, status, header_value, points, message}</code>.</li>
		<li><strong>score_results()</strong> in <code>scoring.py</code> sums penalties (negative points) and bonuses
			(positive points), applies them to a baseline of 100, and looks up the corresponding letter grade.</li>
		<li><strong>JSON response</strong> &mdash; Flask returns <code>{status, score, grade, headers, redirect_chain, tests, &hellip;}</code>.</li>
		<li><strong>scan.php upserts</strong> &mdash; the URL row is updated (or inserted), <code>scan_count</code> is
			incremented, and <code>last_scanned_at</code> is bumped to <code>datetime('now')</code>.</li>
		<li><strong>Persist</strong> &mdash; one row is inserted into <code>scans</code>, then one row per rule into
			<code>scan_tests</code>. Raw headers and redirect chain are stored as JSON text.</li>
		<li><strong>renderResult(r)</strong> in <code>main.js</code> displays the grade in <code>#grade</code> (its
			<code>data-grade</code> attribute drives the colour), shows the score, and renders the per-rule table.
			<code>loadHistory()</code> is called immediately to refresh the recent-scans table.</li>
	</ol>

	<div class="callout warn">
		<strong>Error path.</strong>
		If <code>requests.get</code> raises <code>RequestException</code> (DNS failure, timeout, connection refused), the
		analyzer still returns HTTP 200 with <code>{status: "error", error_message: &hellip;}</code>. <code>scan.php</code>
		records the error in the <code>scans.error_message</code> column with <code>status = 'error'</code> and skips
		inserting <code>scan_tests</code> rows. The UI shows the error in the meta line.
	</div>
</section>

<!-- ============================================================ -->
<section id="analyzer">
	<h2>6. Python Analyzer Component</h2>

	<h3>6.1 <code>analyzer/app.py</code></h3>
	<p>The entry point. Builds a Flask application with two routes.</p>
	<table>
		<thead><tr><th>Function / Route</th><th>Purpose</th></tr></thead>
		<tbody>
			<tr>
				<td><code>fetch(url)</code></td>
				<td>Wraps <code>requests.get</code>. Returns a dict containing the status code, final URL, full headers,
					the list of redirect URLs (<code>r.history</code> + <code>r.url</code>), every
					<code>Set-Cookie</code> value, the content type and the HTML body (only when content type contains
					&ldquo;html&rdquo;). The 10-second <code>TIMEOUT</code> constant guards against hung connections.</td>
			</tr>
			<tr>
				<td><code>POST /scan</code></td>
				<td>JSON in: <code>{url}</code>. Validates input, calls <code>fetch()</code>, builds a
					<code>context</code> dict, iterates <code>ALL_RULES</code>, hands the results to
					<code>score_results()</code>, and returns the assembled JSON.</td>
			</tr>
			<tr>
				<td><code>GET /health</code></td>
				<td>Liveness probe. Returns <code>{"ok": true}</code>.</td>
			</tr>
		</tbody>
	</table>

	<h3>6.2 <code>analyzer/scoring.py</code></h3>
	<p>Pure logic with no external dependencies.</p>
	<ul>
		<li><code>BASELINE_SCORE = 100</code>, <code>MIN_SCORE = 0</code>, <code>MAX_SCORE = 145</code>.</li>
		<li><code>grade(score)</code> &mdash; chained <code>if</code>/<code>elif</code> threshold lookup. See
			<a href="#scoring">Scoring &amp; Grading</a> for the full table.</li>
		<li><code>score_results(results)</code> &mdash; sums penalties and bonuses separately. Bonuses only apply if the
			score is already &ge; 90 (the Observatory rule that bonuses cannot rescue a failing site). Clamps the
			result to <code>[MIN_SCORE, MAX_SCORE]</code> and returns <code>(score, grade)</code>.</li>
	</ul>

	<h3>6.3 <code>analyzer/rules/</code> &mdash; the rule engine</h3>
	<p>Every rule is a Python module with the same contract:</p>
	<pre><code>def check(headers: dict, context: dict) -&gt; dict:
    return {
        "header_name":  str,                    # name of the header being judged
        "status":       "Present" | "Missing" | "Misconfigured",
        "header_value": str | None,             # echoed back so the UI can show it
        "points":       int,                    # negative = penalty, positive = bonus
        "message":      str,                    # short kebab-case reason code
    }</code></pre>
	<p>The <code>context</code> dict carries everything that isn&rsquo;t a plain header value &mdash; final URL, redirect chain,
	parsed Set-Cookie values, HTML body and content type. <code>rules/__init__.py</code> imports every rule module and
	exports the <code>ALL_RULES</code> list. <em>To add a new check, write a new module and append it to that list.</em></p>

	<div class="callout tip">
		<strong>Why one module per header?</strong>
		Each header has its own RFCs, edge cases and historical baggage. Putting each in its own file keeps the rule
		logic readable and makes per-rule testing straightforward.
	</div>
</section>

<!-- ============================================================ -->
<section id="web">
	<h2>7. PHP Web Layer Component</h2>
	<p>All PHP code lives under <code>web/</code>. The UI sits at the root (<code>index.php</code>); JSON endpoints sit
	under <code>web/api/</code>; reusable helpers sit under <code>web/lib/</code>.</p>

	<h3>7.1 <code>web/index.php</code></h3>
	<p>The single HTML page. It begins with <code>require_once "lib/db.php"</code> so that hitting the page on first
	use creates the SQLite schema before the JavaScript starts firing API requests. The page has four sections:</p>
	<ul>
		<li><code>&lt;form id="scan-form"&gt;</code> &mdash; URL input + Scan button</li>
		<li><code>#result</code> &mdash; grade box and per-header results table (hidden until first scan)</li>
		<li><code>.history</code> &mdash; recent scans table + Compare button</li>
		<li><code>#compare-result</code> &mdash; diff output (hidden until Compare is clicked)</li>
	</ul>

	<h3>7.2 <code>web/lib/db.php</code> &mdash; the canonical DB layer</h3>
	<p>Creates a PDO connection to <code>http_intercept_db.sqlite</code> in the same folder, sets
	<code>ATTR_ERRMODE = EXCEPTION</code>, sets the default fetch mode to associative arrays, and enables
	<code>PRAGMA foreign_keys = ON</code>. Then it calls <code>createTables($con)</code>, which idempotently creates
	<code>urls</code> &rarr; <code>scans</code> &rarr; <code>scan_tests</code> (in that order so the foreign keys are
	satisfied).</p>
	<p>Two small utilities are provided but currently unused at runtime: <code>columnExists()</code> and
	<code>addColumnIfMissing()</code>. They exist so that future migrations can be done in-place without rebuilding the
	database file.</p>

	<h3>7.3 <code>web/lib/analyzer_client.php</code></h3>
	<ul>
		<li><code>analyzer_url()</code> &mdash; returns the analyzer base URL from <code>$_ENV["ANALYZER_URL"]</code> if
			set, otherwise <code>http://127.0.0.1:5000</code>.</li>
		<li><code>analyzer_scan($url)</code> &mdash; cURL POST with a 30-second timeout, JSON content type, JSON-decoded
			return. Wraps transport failures into <code>{status: "error", error_message}</code> so callers don&rsquo;t
			need to distinguish network failures from analyzer-reported errors.</li>
	</ul>

	<h3>7.4 <code>web/lib/sanitize.php</code></h3>
	<ul>
		<li><code>clean_url($input)</code> &mdash; trims, prefixes <code>http://</code> if no scheme, validates with
			<code>FILTER_VALIDATE_URL</code>, ensures a host is parseable, returns <code>null</code> on failure.</li>
		<li><code>host_of($url)</code> &mdash; <code>parse_url(&hellip;, PHP_URL_HOST)</code>.</li>
		<li><code>clean_int($input, $default = 0)</code> &mdash; safe integer cast for query-string IDs.</li>
	</ul>

	<h3>7.5 <code>web/api/</code> &mdash; the three JSON endpoints</h3>
	<p>See <a href="#api">section 12</a> for the full request/response contracts. In summary:</p>
	<ul>
		<li><code>scan.php</code> &mdash; POST endpoint that triggers a scan via the analyzer and persists everything.</li>
		<li><code>history.php</code> &mdash; GET endpoint that returns either the URL list (no query string) or the
			scan list for one URL (<code>?url=&hellip;</code>).</li>
		<li><code>compare.php</code> &mdash; GET endpoint that loads two scans by ID, builds a per-header diff, and
			returns <code>{a, b, diff}</code>.</li>
	</ul>
</section>

<!-- ============================================================ -->
<section id="frontend">
	<h2>8. Frontend Component</h2>
	<p>The frontend is intentionally tiny &mdash; one HTML file, one JS file, one CSS file. No framework, no build step.</p>

	<h3>8.1 <code>web/public/main.js</code></h3>
	<table>
		<thead><tr><th>Function</th><th>Behaviour</th></tr></thead>
		<tbody>
			<tr><td><code>onScan(e)</code></td><td>Posts the URL to <code>api/scan.php</code>, then calls
				<code>renderResult()</code> and <code>loadHistory()</code>.</td></tr>
			<tr><td><code>renderResult(r)</code></td><td>Sets <code>#grade</code>&rsquo;s text and
				<code>data-grade</code> attribute (which the CSS uses for colour), fills the score and meta, and
				populates the tests table.</td></tr>
			<tr><td><code>loadHistory()</code></td><td>Fetches <code>api/history.php</code> and renders the URL list with
				a checkbox per row. Wires up the change handler that drives selection.</td></tr>
			<tr><td><code>onPick(e)</code></td><td>Maintains a <code>Set</code> of selected URLs (max 2), enables the
				Compare button when exactly two are picked.</td></tr>
			<tr><td><code>onCompare()</code></td><td>Resolves each URL to its latest <code>scan_id</code> via
				<code>history.php?url=&hellip;</code>, then calls <code>compare.php?a=&hellip;&b=&hellip;</code>.</td></tr>
			<tr><td><code>renderCompare(data)</code></td><td>Renders the diff table, applying a <code>.changed</code>
				class to rows whose status / value / points differ between A and B.</td></tr>
			<tr><td><code>escapeHtml(s)</code></td><td>Defensive HTML escaping (&amp; &lt; &gt; &quot; &#39;) so that
				adversarial header values cannot inject markup.</td></tr>
		</tbody>
	</table>

	<h3>8.2 <code>web/public/style.css</code></h3>
	<p>A dark theme (background <code>#0f1115</code>, text <code>#e6e6e6</code>). The most interesting fragment is the
	grade-colour selector chain &mdash; <code>.grade[data-grade="A+"]</code> through <code>F</code> each set a unique
	background colour, so the JS just sets <code>data-grade</code> and the CSS does the rest.</p>
</section>

<!-- ============================================================ -->
<section id="database">
	<h2>9. Database Design</h2>

	<h3>9.1 Tables and relationships</h3>
	<div class="er-diagram">
		<div class="er-table">
			<div class="er-title">urls</div>
			<ul>
				<li><span class="pk">url_id</span> &middot; INTEGER PK AUTOINCREMENT</li>
				<li>url &middot; TEXT UNIQUE</li>
				<li>hostname &middot; TEXT</li>
				<li>first_scanned_at &middot; TEXT</li>
				<li>last_scanned_at &middot; TEXT</li>
				<li>scan_count &middot; INTEGER</li>
			</ul>
		</div>
		<div class="er-relation">1 &rarr; N</div>
		<div class="er-table">
			<div class="er-title">scans</div>
			<ul>
				<li><span class="pk">scan_id</span> &middot; INTEGER PK</li>
				<li><span class="fk">url_id</span> &middot; FK &rarr; urls.url_id</li>
				<li>status &middot; 'success' | 'error'</li>
				<li>score &middot; INTEGER</li>
				<li>grade &middot; TEXT</li>
				<li>final_url &middot; TEXT</li>
				<li>status_code &middot; INTEGER</li>
				<li>raw_headers_json &middot; TEXT</li>
				<li>redirect_chain_json &middot; TEXT</li>
				<li>error_message &middot; TEXT</li>
				<li>scanned_at &middot; TEXT</li>
			</ul>
		</div>
		<div class="er-relation">1 &rarr; N</div>
		<div class="er-table">
			<div class="er-title">scan_tests</div>
			<ul>
				<li><span class="pk">test_id</span> &middot; INTEGER PK</li>
				<li><span class="fk">scan_id</span> &middot; FK &rarr; scans.scan_id</li>
				<li>header_name &middot; TEXT</li>
				<li>status &middot; 'Present' | 'Missing' | 'Misconfigured'</li>
				<li>header_value &middot; TEXT</li>
				<li>points &middot; INTEGER</li>
				<li>message &middot; TEXT</li>
			</ul>
		</div>
	</div>

	<h3>9.2 Cascade behaviour</h3>
	<p>Both foreign keys use <code>ON DELETE CASCADE</code>. Deleting a URL from <code>urls</code> wipes every scan and
	every per-rule test for that URL in a single statement. This requires <code>PRAGMA foreign_keys = ON</code>, which
	<code>web/lib/db.php</code> sets unconditionally on every connection.</p>

	<h3>9.3 Schema bootstrap</h3>
	<p><code>createTables()</code> is idempotent thanks to <code>CREATE TABLE IF NOT EXISTS</code>. The tables are
	created in the order <code>urls</code> &rarr; <code>scans</code> &rarr; <code>scan_tests</code> so that the
	foreign-key constraints reference tables that already exist.</p>

	<h3>9.4 What goes where</h3>
	<table>
		<thead><tr><th>Concern</th><th>Stored in</th></tr></thead>
		<tbody>
			<tr><td>The list of tracked URLs and how often each has been scanned</td><td><code>urls</code></td></tr>
			<tr><td>One row per scan attempt, with grade and raw headers</td><td><code>scans</code></td></tr>
			<tr><td>One row per rule outcome per scan</td><td><code>scan_tests</code></td></tr>
			<tr><td>Comparisons (derived on-the-fly)</td><td>not stored &mdash; <code>compare.php</code> reads from <code>scan_tests</code></td></tr>
		</tbody>
	</table>
</section>

<!-- ============================================================ -->
<section id="rules">
	<h2>10. Security Rules &mdash; Per-Header Detail</h2>
	<p>Every rule below lives in <code>analyzer/rules/</code> and is registered in <code>ALL_RULES</code>. The tables
	enumerate the concrete outcomes a rule can return &mdash; the <code>message</code> string is the kebab-case identifier
	emitted by each branch, and the <code>points</code> column shows the score impact applied by
	<code>score_results()</code>.</p>

	<!-- ============================== HSTS ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.1 Strict-Transport-Security (HSTS)</h3>
			<div class="rule-file">analyzer/rules/hsts.py</div>
		</div>
		<div class="rule-body">
			<p>Forces browsers to use HTTPS for a set duration. The rule first checks whether the final URL is HTTPS at
			all; if not, the header is moot. It then parses <code>max-age</code> and, if all <code>preload</code> /
			<code>includeSubDomains</code> / <code>max-age &ge; 1 year</code> conditions are met, awards a bonus.</p>
			<table>
				<thead><tr><th>Outcome (<code>message</code>)</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>hsts-not-implemented-no-https</td><td>Missing</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>hsts-not-implemented</td><td>Missing</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>hsts-header-invalid (cannot parse / max-age missing)</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>hsts-implemented-max-age-less-than-six-months</td><td>Misconfigured</td><td class="points-neg">&minus;10</td></tr>
					<tr><td>hsts-implemented-max-age-at-least-six-months</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>hsts-preloaded (preload + includeSubDomains + max-age &ge; 1 yr)</td><td>Present</td><td class="points-pos">+5</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== CSP ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.2 Content-Security-Policy (CSP)</h3>
			<div class="rule-file">analyzer/rules/csp.py</div>
		</div>
		<div class="rule-body">
			<p>The most elaborate rule. <code>_parse()</code> splits the policy on <code>;</code> and groups sources by
			directive. The check then layers tests for <code>unsafe-inline</code> / <code>unsafe-eval</code>, insecure
			schemes (<code>http:</code>) in active vs. passive directives, broad wildcards in
			<code>script-src</code> / <code>object-src</code>, and a bonus condition (<code>default-src 'none'</code>
			plus a safe <code>form-action</code>).</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>csp-not-implemented</td><td>Missing</td><td class="points-neg">&minus;25</td></tr>
					<tr><td>csp-not-implemented-but-reporting-enabled (Report-Only only)</td><td>Misconfigured</td><td class="points-neg">&minus;25</td></tr>
					<tr><td>csp-header-invalid (cannot parse / no directives)</td><td>Misconfigured</td><td class="points-neg">&minus;25</td></tr>
					<tr><td>csp-implemented-with-unsafe-inline (script-src/object-src unsafe)</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>csp-implemented-with-insecure-scheme</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>csp-implemented-with-insecure-scheme-in-passive-content-only</td><td>Misconfigured</td><td class="points-neg">&minus;10</td></tr>
					<tr><td>csp-implemented-with-unsafe-eval</td><td>Misconfigured</td><td class="points-neg">&minus;10</td></tr>
					<tr><td>csp-implemented-with-unsafe-inline-in-style-src-only</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>csp-implemented-with-no-unsafe</td><td>Present</td><td class="points-pos">+5</td></tr>
					<tr><td>csp-implemented-with-no-unsafe-default-src-none (+ safe form-action)</td><td>Present</td><td class="points-pos">+10</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== X-Frame-Options ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.3 X-Frame-Options</h3>
			<div class="rule-file">analyzer/rules/x_frame_options.py</div>
		</div>
		<div class="rule-body">
			<p>Defends against clickjacking. Accepts CSP <code>frame-ancestors</code> as a valid modern replacement (no
			penalty if found in the CSP).</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>x-frame-options-implemented-via-csp</td><td>Present</td><td class="points-pos">+5</td></tr>
					<tr><td>x-frame-options-sameorigin-or-deny</td><td>Present</td><td class="points-pos">+5</td></tr>
					<tr><td>x-frame-options-allow-from-origin</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>x-frame-options-not-implemented</td><td>Missing</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>x-frame-options-header-invalid</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== X-Content-Type-Options ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.4 X-Content-Type-Options</h3>
			<div class="rule-file">analyzer/rules/x_content_type_options.py</div>
		</div>
		<div class="rule-body">
			<p>Single-purpose header. The only valid value is <code>nosniff</code>.</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>x-content-type-options-nosniff</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>x-content-type-options-not-implemented</td><td>Missing</td><td class="points-neg">&minus;5</td></tr>
					<tr><td>x-content-type-options-header-invalid</td><td>Misconfigured</td><td class="points-neg">&minus;5</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== Referrer-Policy ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.5 Referrer-Policy</h3>
			<div class="rule-file">analyzer/rules/referrer_policy.py</div>
		</div>
		<div class="rule-body">
			<p>The browser uses the <em>last</em> token in a comma-separated list, so the rule evaluates
			<code>tokens[-1]</code> against safe and unsafe sets.</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>referrer-policy-private (no-referrer / same-origin / strict-origin*)</td><td>Present</td><td class="points-pos">+5</td></tr>
					<tr><td>referrer-policy-not-implemented</td><td>Missing</td><td class="points-zero">0</td></tr>
					<tr><td>referrer-policy-unsafe (origin / unsafe-url / &hellip;)</td><td>Misconfigured</td><td class="points-neg">&minus;5</td></tr>
					<tr><td>referrer-policy-header-invalid (unknown token)</td><td>Misconfigured</td><td class="points-neg">&minus;5</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== Set-Cookie ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.6 Set-Cookie (cookie flags)</h3>
			<div class="rule-file">analyzer/rules/set_cookie.py</div>
		</div>
		<div class="rule-body">
			<p>Inspects every cookie returned by the target. Tests for <code>Secure</code>, <code>HttpOnly</code>,
			<code>SameSite</code> validity, an anti-CSRF naming hint without <code>SameSite</code>, and the
			interplay with HSTS. The penalty selected is the first matching condition (worst wins).</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>cookies-not-found</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>cookies-session-without-secure-flag</td><td>Misconfigured</td><td class="points-neg">&minus;40</td></tr>
					<tr><td>cookies-session-without-httponly-flag</td><td>Misconfigured</td><td class="points-neg">&minus;30</td></tr>
					<tr><td>cookies-samesite-flag-invalid</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>cookies-anticsrf-without-samesite-flag</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>cookies-without-secure-flag (no HSTS)</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>cookies-session-without-secure-flag-but-protected-by-hsts</td><td>Misconfigured</td><td class="points-neg">&minus;10</td></tr>
					<tr><td>cookies-without-secure-flag-but-protected-by-hsts</td><td>Misconfigured</td><td class="points-neg">&minus;5</td></tr>
					<tr><td>cookies-secure-with-httponly-sessions</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>cookies-secure-with-httponly-sessions-and-samesite</td><td>Present</td><td class="points-pos">+5</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== CORS ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.7 Access-Control-Allow-Origin (CORS)</h3>
			<div class="rule-file">analyzer/rules/cors.py</div>
		</div>
		<div class="rule-body">
			<p>Mostly informational. The dangerous case is <code>ACAO: *</code> together with
			<code>Access-Control-Allow-Credentials: true</code>, which most browsers refuse but is heavily penalised
			anyway.</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>cross-origin-resource-sharing-not-implemented</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>cross-origin-resource-sharing-implemented-with-restricted-access</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>cross-origin-resource-sharing-implemented-with-public-access (*)</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>cross-origin-resource-sharing-implemented-with-universal-access</td><td>Misconfigured</td><td class="points-neg">&minus;50</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== CORP ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.8 Cross-Origin-Resource-Policy (CORP)</h3>
			<div class="rule-file">analyzer/rules/corp.py</div>
		</div>
		<div class="rule-body">
			<p>Restricts which origins may embed the response as a resource. Bonus is awarded for the two strict
			values.</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>corp-not-implemented (defaults to cross-origin)</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>corp-implemented-with-same-origin</td><td>Present</td><td class="points-pos">+10</td></tr>
					<tr><td>corp-implemented-with-same-site</td><td>Present</td><td class="points-pos">+10</td></tr>
					<tr><td>corp-implemented-with-cross-origin</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>corp-header-invalid</td><td>Misconfigured</td><td class="points-neg">&minus;5</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== HTTPS Redirect ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.9 HTTP &rarr; HTTPS Redirection</h3>
			<div class="rule-file">analyzer/rules/https_redirect.py</div>
		</div>
		<div class="rule-body">
			<p>Synthetic rule with no single header. Inspects the redirect chain captured by
			<code>fetch()</code>. The worst-case finding is that the site is plain HTTP only; the cleanest is a
			same-host HTTPS redirect on the very first hop, which lets HSTS take effect.</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>redirection-not-needed-no-http (already HTTPS)</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>redirection-to-https</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>redirection-off-host-from-http (first hop on different host)</td><td>Misconfigured</td><td class="points-neg">&minus;5</td></tr>
					<tr><td>redirection-not-to-https-on-initial-redirection</td><td>Misconfigured</td><td class="points-neg">&minus;10</td></tr>
					<tr><td>redirection-not-to-https (final dest is HTTP)</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>redirection-missing</td><td>Missing</td><td class="points-neg">&minus;20</td></tr>
				</tbody>
			</table>
		</div>
	</article>

	<!-- ============================== SRI ============================== -->
	<article class="rule-card">
		<div class="rule-head">
			<h3>10.10 Subresource Integrity (SRI)</h3>
			<div class="rule-file">analyzer/rules/subresource_integrity.py</div>
		</div>
		<div class="rule-body">
			<p>The only rule that inspects the HTML body. Uses regex
			(<code>SCRIPT_TAG_RE</code>, <code>ATTR_RE</code>) to find <code>&lt;script src&gt;</code> tags and
			determine which ones are external and whether each has an <code>integrity=</code> attribute. Non-HTML
			responses skip the check.</p>
			<table>
				<thead><tr><th>Outcome</th><th>Status</th><th>Points</th></tr></thead>
				<tbody>
					<tr><td>sri-not-implemented-response-not-html</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>sri-not-implemented-but-no-scripts-loaded</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>sri-not-implemented-but-all-scripts-loaded-from-secure-origin (same host)</td><td>Present</td><td class="points-zero">0</td></tr>
					<tr><td>sri-not-implemented-but-external-scripts-loaded-securely</td><td>Misconfigured</td><td class="points-neg">&minus;5</td></tr>
					<tr><td>sri-implemented-but-external-scripts-not-loaded-securely</td><td>Misconfigured</td><td class="points-neg">&minus;20</td></tr>
					<tr><td>sri-not-implemented-and-external-scripts-not-loaded-securely</td><td>Misconfigured</td><td class="points-neg">&minus;50</td></tr>
					<tr><td>sri-implemented-and-external-scripts-loaded-securely</td><td>Present</td><td class="points-pos">+5</td></tr>
				</tbody>
			</table>
		</div>
	</article>
</section>

<!-- ============================================================ -->
<section id="scoring">
	<h2>11. Scoring &amp; Grading System</h2>

	<h3>11.1 The algorithm</h3>
	<ol>
		<li>Start at <code>BASELINE_SCORE = 100</code>.</li>
		<li>Sum all <em>negative</em> points returned by the rules &rarr; <code>penalties</code>.</li>
		<li>Sum all <em>positive</em> points returned by the rules &rarr; <code>bonuses</code>.</li>
		<li>Apply penalties: <code>score = 100 + penalties</code>.</li>
		<li><em>Only if the resulting score is &ge; 90</em>, add bonuses on top. This is the &ldquo;you must earn the
			right to bonuses&rdquo; rule borrowed from Mozilla Observatory.</li>
		<li>Clamp to <code>[0, 145]</code>.</li>
		<li>Convert to a letter grade.</li>
	</ol>
	<pre><code>score = BASELINE_SCORE + penalties
if score &gt;= 90:
    score += bonuses
score = max(MIN_SCORE, min(MAX_SCORE, score))</code></pre>

	<h3>11.2 Grade thresholds (<code>scoring.grade()</code>)</h3>
	<table>
		<thead><tr><th>Score</th><th>Grade</th><th>Score</th><th>Grade</th></tr></thead>
		<tbody>
			<tr><td>&ge; 100</td><td>A+</td><td>50&ndash;59</td><td>C</td></tr>
			<tr><td>90&ndash;99</td><td>A</td><td>45&ndash;49</td><td>C&minus;</td></tr>
			<tr><td>85&ndash;89</td><td>A&minus;</td><td>40&ndash;44</td><td>D+</td></tr>
			<tr><td>80&ndash;84</td><td>B+</td><td>30&ndash;39</td><td>D</td></tr>
			<tr><td>70&ndash;79</td><td>B</td><td>25&ndash;29</td><td>D&minus;</td></tr>
			<tr><td>65&ndash;69</td><td>B&minus;</td><td>&lt; 25</td><td>F</td></tr>
			<tr><td>60&ndash;64</td><td>C+</td><td>&nbsp;</td><td>&nbsp;</td></tr>
		</tbody>
	</table>
</section>

<!-- ============================================================ -->
<section id="api">
	<h2>12. HTTP API Endpoints</h2>

	<h3>12.1 PHP-side (consumed by the browser)</h3>
	<table>
		<thead><tr><th>Method</th><th>Path</th><th>Request</th><th>Response</th></tr></thead>
		<tbody>
			<tr>
				<td>POST</td>
				<td><code>web/api/scan.php</code></td>
				<td>JSON body <code>{ "url": "&hellip;" }</code></td>
				<td><code>{ scan_id, url_id, result: { status, score, grade, headers, tests, &hellip; } }</code></td>
			</tr>
			<tr>
				<td>GET</td>
				<td><code>web/api/history.php</code></td>
				<td>(none)</td>
				<td><code>{ urls: [ { url_id, url, hostname, last_scanned_at, scan_count, latest_score, latest_grade }, &hellip; ] }</code></td>
			</tr>
			<tr>
				<td>GET</td>
				<td><code>web/api/history.php?url=&hellip;</code></td>
				<td>query string <code>url</code></td>
				<td><code>{ url, scans: [ { scan_id, status, score, grade, final_url, status_code, scanned_at, &hellip; }, &hellip; ] }</code></td>
			</tr>
			<tr>
				<td>GET</td>
				<td><code>web/api/compare.php?a=&lt;id&gt;&amp;b=&lt;id&gt;</code></td>
				<td>two scan IDs</td>
				<td><code>{ a, b, diff: [ { header_name, a, b, changed }, &hellip; ] }</code></td>
			</tr>
		</tbody>
	</table>

	<h3>12.2 Python-side (consumed by PHP)</h3>
	<table>
		<thead><tr><th>Method</th><th>Path</th><th>Purpose</th></tr></thead>
		<tbody>
			<tr>
				<td>POST</td>
				<td><code>http://127.0.0.1:5000/scan</code></td>
				<td>Run a scan, return <code>{ status, score, grade, headers, redirect_chain, tests, &hellip; }</code>. No persistence.</td>
			</tr>
			<tr>
				<td>GET</td>
				<td><code>http://127.0.0.1:5000/health</code></td>
				<td>Liveness probe &mdash; returns <code>{ ok: true }</code>.</td>
			</tr>
		</tbody>
	</table>
</section>

<!-- ============================================================ -->
<section id="history-compare">
	<h2>13. History &amp; Compare Flows</h2>

	<h3>13.1 History flow</h3>
	<div class="diagram">
		<div class="flow-row">
			<div class="flow-box ext">main.js<span class="sub">loadHistory()</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box php">history.php<span class="sub">no query string</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box db">SQL: SELECT&hellip; latest score per URL</div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box ext">render table<span class="sub">checkbox per row</span></div>
		</div>
	</div>
	<p>The SELECT uses a correlated subquery to pick the latest <code>score</code> and <code>grade</code> per URL
	without joining the full <code>scans</code> table twice. Results are limited to the 200 most-recently-scanned URLs.</p>

	<h3>13.2 Compare flow</h3>
	<div class="diagram">
		<div class="flow-row">
			<div class="flow-box ext">User picks 2 rows<span class="sub">onPick()</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box ext">onCompare()<span class="sub">main.js</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box php">history.php?url=&hellip;<span class="sub">x2 in parallel</span></div>
		</div>
		<span class="flow-arrow down">&darr;</span>
		<div class="flow-row">
			<div class="flow-box ext">extract latest scan_id<span class="sub">per URL</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box php">compare.php?a=&hellip;&b=&hellip;<span class="sub">load + diff</span></div>
			<span class="flow-arrow">&rarr;</span>
			<div class="flow-box ext">renderCompare()<span class="sub">.changed rows highlighted</span></div>
		</div>
	</div>
	<p>For each header name that appears in either scan, <code>compare.php</code> compares <code>status</code>,
	<code>header_value</code> and <code>points</code>. Any difference flips the <code>changed</code> flag, which the JS
	uses to tint the diff row.</p>
</section>

<!-- ============================================================ -->
<section id="setup">
	<h2>14. Setup &amp; Run Instructions</h2>
	<p>Detailed steps are in <code>STEPS.md</code>. Summary:</p>
	<h4>Prerequisites</h4>
	<ul>
		<li>XAMPP with PHP 8.x (enable <code>pdo_sqlite</code> and <code>curl</code> in <code>php.ini</code>)</li>
		<li>Python 3.9+</li>
		<li>The project must live under <code>htdocs</code> (already at <code>c:\xampp\htdocs\http_intercept\</code>)</li>
	</ul>

	<h4>Start the analyzer</h4>
<pre><code>cd analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py            # listens on http://127.0.0.1:5000</code></pre>

	<h4>Start the web layer</h4>
	<ol>
		<li>Start Apache from the XAMPP Control Panel.</li>
		<li>Open <code>http://localhost/http_intercept/web/</code> in a browser.</li>
		<li>Type a URL, click <em>Scan</em>, watch the grade appear.</li>
	</ol>

	<div class="callout tip">
		<strong>Configuration knob.</strong>
		Setting the environment variable <code>ANALYZER_URL</code> before starting Apache changes where PHP looks for
		the Flask service. Useful for running the analyzer on a non-default port or a different host.
	</div>
</section>

<!-- ============================================================ -->
<section id="extending">
	<h2>15. Extending the Project</h2>

	<h3>15.1 Adding a new security header check</h3>
	<ol>
		<li>Create <code>analyzer/rules/&lt;your_header&gt;.py</code>.</li>
		<li>Implement <code>def check(headers, context) -&gt; dict</code> following the contract in &sect;6.3.</li>
		<li>Import the module in <code>analyzer/rules/__init__.py</code> and append <code>&lt;your_header&gt;.check</code>
			to the <code>ALL_RULES</code> list.</li>
		<li>Restart Flask. No PHP or database changes are required &mdash; <code>scan.php</code> persists whatever rule
			outcomes the analyzer returns.</li>
	</ol>

	<h3>15.2 Adding a database column</h3>
	<ol>
		<li>Decide which table needs the column.</li>
		<li>Use <code>addColumnIfMissing($con, $table, $column, $definition)</code> in <code>db.php</code> (it&rsquo;s
			already implemented but commented out).</li>
		<li>Update the relevant <code>INSERT</code> in <code>web/api/scan.php</code>.</li>
	</ol>

	<h3>15.3 Reskinning the UI</h3>
	<p>The frontend has no build step. Edit <code>web/public/style.css</code> directly and refresh the browser. The
	grade colour is driven by the <code>data-grade</code> attribute on <code>#grade</code>, so per-grade theme tweaks
	live in the CSS only.</p>

	<h3>15.4 Adding a new API endpoint</h3>
	<ol>
		<li>Create a new PHP file under <code>web/api/</code>.</li>
		<li><code>require_once</code> the helpers from <code>web/lib/</code> (always <code>db.php</code>, plus
			<code>sanitize.php</code> for input handling).</li>
		<li>Return JSON with <code>header("Content-Type: application/json")</code> and <code>echo json_encode(&hellip;)</code>.</li>
		<li>Call it from <code>main.js</code> with <code>fetch()</code>.</li>
	</ol>
</section>

<footer class="doc-footer">
	http_intercept &middot; Project Structure &amp; Flow Documentation &middot; based on the contents of
	<code>analyzer/</code>, <code>web/</code>, <code>CLAUDE.md</code>, <code>README.md</code> and <code>STEPS.md</code>.
</footer>

</body>
</html>