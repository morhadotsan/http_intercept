def check(headers, context):
    name = "X-Frame-Options"
    value = headers.get(name)
    csp = (headers.get("Content-Security-Policy") or "").lower()

    if "frame-ancestors" in csp:
        return {"header_name": name, "status": "Present", "header_value": value or "(via CSP frame-ancestors)",
                "points": 5, "message": "x-frame-options-implemented-via-csp."}

    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": -20, "message": "x-frame-options-not-implemented."}

    v = value.strip().upper()
    if v in ("DENY", "SAMEORIGIN"):
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "x-frame-options-sameorigin-or-deny."}

    if v.startswith("ALLOW-FROM"):
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 0, "message": "x-frame-options-allow-from-origin."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": -20, "message": "x-frame-options-header-invalid."}
