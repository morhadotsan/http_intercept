# http_intercept

A self-hosted HTTP security-header scanner — a local clone of [Mozilla Observatory](https://developer.mozilla.org/en-US/observatory).

Submit any URL and http_intercept fetches its HTTP response, evaluates the response headers against a catalogue of security best practices, assigns a letter grade (A+ → F), and persists the result so you can track improvements over time.

---

## Features

- **Scan** — fetch a URL's headers and run them through ten security rules
- **Grade** — convert rule outcomes into a numeric score and a letter grade (A+ → F)
- **History** — browse every previously scanned URL with its latest grade
- **Compare** — diff the headers of any two scanned URLs side by side

---

## Stack

| Layer | Technology |
|---|---|
| Analyzer | Python 3.9+ · Flask · `requests` |
| Web UI & API | PHP 8.x · Apache (XAMPP) |
| Persistence | SQLite 3 (file-based, no server needed) |

---

## Project Structure

```
http_intercept/
├── analyzer/                        # Python (Flask) — runs as a separate process
│   ├── app.py                       # POST /scan · GET /health
│   ├── scoring.py                   # Converts rule points into a letter grade
│   ├── requirements.txt             # Flask==3.0.3, requests==2.32.3
│   └── rules/                       # One module per security header
│       ├── __init__.py              # Registers ALL_RULES
│       ├── corp.py                  # Cross-Origin-Resource-Policy
│       ├── cors.py                  # Access-Control-Allow-Origin / Allow-Credentials
│       ├── csp.py                   # Content-Security-Policy
│       ├── hsts.py                  # Strict-Transport-Security
│       ├── https_redirect.py        # HTTP → HTTPS redirect health
│       ├── referrer_policy.py       # Referrer-Policy
│       ├── set_cookie.py            # Secure / HttpOnly / SameSite cookie flags
│       ├── subresource_integrity.py # External <script integrity=…> checks
│       ├── x_content_type_options.py# X-Content-Type-Options: nosniff
│       └── x_frame_options.py       # X-Frame-Options / CSP frame-ancestors
├── web/                             # PHP layer — served by XAMPP Apache
│   ├── index.php                    # Single-page UI
│   ├── api/
│   │   ├── scan.php                 # POST: run a scan and persist results
│   │   ├── history.php              # GET: list URLs or scans for one URL
│   │   └── compare.php              # GET: diff two scan IDs
│   ├── lib/
│   │   ├── db.php                   # PDO connection + schema bootstrap
│   │   ├── analyzer_client.php      # cURL bridge to the Flask analyzer
│   │   ├── sanitize.php             # clean_url(), host_of(), clean_int()
│   │   └── http_intercept_db.sqlite # SQLite database (auto-created)
│   └── public/
│       ├── main.js                  # UI controller (Fetch API)
│       └── style.css                # Dark theme
├── documentation/
│   ├── project_structure.html       # Full architecture & flow documentation
│   └── style.css
├── README.md
└── STEPS.md                         # Setup & usage guide
```

---

## Quick Start

Full instructions are in [`STEPS.md`](STEPS.md). In brief:

**1. Start the Python analyzer**
```bash
cd analyzer
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                 # Listens on http://127.0.0.1:5000
```

**2. Start the web layer**

Start Apache from the XAMPP Control Panel, then open:
```
http://localhost/http_intercept/web/
```

Type a URL and click **Scan**.

---

## How It Works

The browser talks only to PHP; PHP forwards the scan to the Flask analyzer; the analyzer fetches the target URL and runs the rules. SQLite is written exclusively by the PHP layer — the analyzer is stateless.

```
Browser → PHP (Apache) → Python Analyzer → Target website
                ↓
            SQLite
```

Each of the ten rules returns a `pass/fail/info` status and a point value. `scoring.py` sums the points and maps the total to a letter grade using the same scale as Mozilla Observatory.