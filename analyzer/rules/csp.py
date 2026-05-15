def check(headers, context):
    name = "Content-Security-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "No Content-Security-Policy set."}

    lower = value.lower()
    if "'unsafe-inline'" in lower or "'unsafe-eval'" in lower:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": 5, "message": "CSP allows 'unsafe-inline' or 'unsafe-eval'."}

    if "default-src" not in lower and "script-src" not in lower:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": 5, "message": "CSP missing default-src or script-src directive."}

    return {"header_name": name, "status": "Present", "header_value": value,
            "points": 25, "message": "CSP looks reasonable."}
