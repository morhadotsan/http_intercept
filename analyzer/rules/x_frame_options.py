def check(headers, context):
    name = "X-Frame-Options"
    value = headers.get(name)
    csp = (headers.get("Content-Security-Policy") or "").lower()
    if "frame-ancestors" in csp:
        return {"header_name": name, "status": "Present", "header_value": value or "(via CSP frame-ancestors)",
                "points": 10, "message": "Clickjacking protected via CSP frame-ancestors."}

    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "X-Frame-Options not set."}

    v = value.strip().upper()
    if v in ("DENY", "SAMEORIGIN"):
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 10, "message": "X-Frame-Options correctly set."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": 3, "message": "X-Frame-Options has an invalid or weak value."}
