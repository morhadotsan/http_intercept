from flask import Flask, request, jsonify
import requests
from rules import ALL_RULES
from scoring import score_results

app = Flask(__name__)
TIMEOUT = 10


def fetch(url):
    r = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
    chain = [resp.url for resp in r.history] + [r.url]
    headers = dict(r.headers)
    set_cookies = []
    if hasattr(r.raw, "headers"):
        try:
            set_cookies = r.raw.headers.get_all("Set-Cookie") or []
        except Exception:
            set_cookies = []
    if not set_cookies and "Set-Cookie" in headers:
        set_cookies = [headers["Set-Cookie"]]
    return {
        "status_code": r.status_code,
        "final_url": r.url,
        "headers": headers,
        "redirect_chain": chain,
        "set_cookies": set_cookies,
    }


@app.route("/scan", methods=["POST"])
def scan():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"status": "error", "error_message": "Missing url"}), 400
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    try:
        fetched = fetch(url)
    except requests.RequestException as e:
        return jsonify({"status": "error", "error_message": str(e), "initial_url": url}), 200

    context = {
        "initial_url": url,
        "final_url": fetched["final_url"],
        "redirect_chain": fetched["redirect_chain"],
        "set_cookies": fetched["set_cookies"],
    }

    results = [rule(fetched["headers"], context) for rule in ALL_RULES]
    score, grade_ = score_results(results)

    return jsonify({
        "status": "success",
        "initial_url": url,
        "final_url": fetched["final_url"],
        "status_code": fetched["status_code"],
        "score": score,
        "grade": grade_,
        "headers": fetched["headers"],
        "redirect_chain": fetched["redirect_chain"],
        "tests": results,
    })


@app.route("/health")
def health():
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
