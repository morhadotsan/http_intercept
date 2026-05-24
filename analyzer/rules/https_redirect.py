from urllib.parse import urlparse


def _host(url):
    try:
        return urlparse(url).hostname or ""
    except Exception:
        return ""


def check(headers, context):
    name = "Redirection"
    initial = context.get("initial_url", "") or ""
    final = context.get("final_url", "") or ""
    chain = context.get("redirect_chain") or []

    if initial.startswith("https://"):
        return {"header_name": name, "status": "Present", "header_value": final,
                "points": 0, "message": "redirection-not-needed-no-http: initial request already HTTPS."}

    if not chain or len(chain) <= 1:
        if final.startswith("http://"):
            return {"header_name": name, "status": "Missing", "header_value": final,
                    "points": -20, "message": "redirection-missing: does not redirect to an HTTPS site."}

    first_hop = chain[1] if len(chain) > 1 else final

    if final.startswith("http://"):
        return {"header_name": name, "status": "Misconfigured", "header_value": final,
                "points": -20, "message": "redirection-not-to-https: final destination is not HTTPS."}

    if first_hop.startswith("http://"):
        return {"header_name": name, "status": "Misconfigured", "header_value": final,
                "points": -10, "message": "redirection-not-to-https-on-initial-redirection."}

    if first_hop.startswith("https://") and _host(first_hop) != _host(initial):
        return {"header_name": name, "status": "Misconfigured", "header_value": final,
                "points": -5, "message": "redirection-off-host-from-http: first hop targets a different host (prevents HSTS)."}

    return {"header_name": name, "status": "Present", "header_value": final,
            "points": 0, "message": "redirection-to-https: initial redirection is to HTTPS on same host."}
