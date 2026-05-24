def check(headers, context):
    name = "Cross-Origin-Resource-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Present", "header_value": None,
                "points": 0, "message": "corp-not-implemented (defaults to cross-origin)."}

    v = value.strip().lower()
    if v == "same-origin":
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 10, "message": "corp-implemented-with-same-origin."}
    if v == "same-site":
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 10, "message": "corp-implemented-with-same-site."}
    if v == "cross-origin":
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 0, "message": "corp-implemented-with-cross-origin."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": -5, "message": "corp-header-invalid."}
