# How to use http_intercept

A self-hosted security-header scanner. Two services run side by side: the **PHP web layer** (UI + API, served by XAMPP) and the **Python analyzer** (Flask, fetches the target URL and grades its headers).

---

## 1. Prerequisites

- **XAMPP** with PHP 8.x — used to serve the `web/` directory
- **Python 3.9+**
- The project must live inside `htdocs`. This repo is already at `c:\xampp\htdocs\http_intercept\`.

Make sure these PHP extensions are enabled in `php.ini` (they ship with XAMPP, just uncomment if needed):
- `extension=pdo_sqlite`
- `extension=curl`

---

## 2. Start the analyzer (Flask)

Open a terminal in the project root and run:

```powershell
cd analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

You should see Flask listening on `http://127.0.0.1:5000`.

Quick check:

```powershell
curl http://127.0.0.1:5000/health
```

Expected: `{"ok": true}`.

> **Custom analyzer host?** Set the `ANALYZER_URL` env var before starting Apache, e.g. `set ANALYZER_URL=http://127.0.0.1:6000`. The PHP layer reads this in `web/lib/analyzer_client.php`.

---

## 3. Start the web layer (XAMPP)

1. Launch the **XAMPP Control Panel**.
2. Click **Start** next to **Apache**.
3. Open your browser at:

   ```
   http://localhost/http_intercept/web/
   ```

The SQLite database (`web/lib/http_intercept_db.sqlite`) is created automatically on first load by `web/lib/db.php`.

---

## 4. Scan a URL

1. Type a URL into the input box (e.g. `https://example.com`).
2. Click **Scan**.
3. The page shows:
   - **Letter grade** (A+ to F) and **score** out of 100
   - The **final URL** and **HTTP status code**
   - A table of every checked header: status (Present / Missing / Misconfigured), value, points, and a short note

Each scan is saved to history automatically.

---

## 5. View history

The **Recent scans** table at the bottom of the page lists every URL you have scanned, with the most recent grade and timestamp.

---

## 6. Compare two scans

1. In the **Recent scans** table, tick the checkbox next to **two** different URLs.
2. The **Compare selected (2)** button becomes active — click it.
3. A diff table appears showing each header side-by-side. Rows where the status, value, or points differ are highlighted.

> Comparison uses the *latest* scan of each selected URL. Re-scan a URL first if you want to compare its newest results.

---

## 7. What gets checked

| Header | What we look for |
|---|---|
| Strict-Transport-Security (HSTS) | Present, `max-age` ≥ 180 days |
| Content-Security-Policy | Present, no `unsafe-inline` / `unsafe-eval`, has `default-src` or `script-src` |
| X-Frame-Options | `DENY` / `SAMEORIGIN`, or CSP `frame-ancestors` |
| X-Content-Type-Options | `nosniff` |
| Referrer-Policy | A safe value (`no-referrer`, `strict-origin`, etc.) |
| Permissions-Policy | Present |
| Cross-Origin-Opener-Policy | `same-origin` / `same-origin-allow-popups` / `same-site` |
| Cross-Origin-Embedder-Policy | `require-corp` / `credentialless` |
| Cross-Origin-Resource-Policy | `same-origin` / `same-site` / `cross-origin` |
| Set-Cookie flags | Every cookie has `Secure`, `HttpOnly`, `SameSite` |
| HTTP → HTTPS redirect | `http://…` requests are redirected to `https://…` |

---

## 8. Endpoints (for scripting)

| Endpoint | Method | Purpose |
|---|---|---|
| `/web/api/scan.php` | POST `{ "url": "..." }` | Run a scan and persist it |
| `/web/api/history.php` | GET (optional `?url=`) | List all URLs, or scans for one URL |
| `/web/api/compare.php?a=ID&b=ID` | GET | Diff two scan IDs |
| `http://127.0.0.1:5000/scan` (analyzer) | POST `{ "url": "..." }` | Direct analyzer call (no persistence) |

---

## 9. Stopping

- Stop Flask: `Ctrl+C` in its terminal.
- Stop Apache: click **Stop** in the XAMPP Control Panel.
