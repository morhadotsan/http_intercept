# http_intercept
This project is http_intercept, a security header scanner, essentially a self-hosted clone of Mozilla Observatory.

http_intercept/
├── analyzer/         # Python (Flask)
│   ├── app.py
│   ├── rules/        # one module per header
│   ├── scoring.py
│   └── requirements.txt
├── web/              # PHP
│   ├── index.php
│   ├── api/          # scan.php, history.php, compare.php
│   ├── lib/          # db.php, analyzer_client.php, sanitize.php
│   └── public/       # css, js, img
└── README.md

The project is to develop a security tool that intercept a HTTP response from a given web server, extracts the header fields and checks if and which security HTTP header fields are implemented by the web server and which are missing.

It will work like https://developer.mozilla.org/en-US/observatory

# Scope of the project
PHP for web layer, Python for the analyzer, SQLite for storing scan history
Scan + grade + save history + compare scans