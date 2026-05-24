def check(headers, context):
    name = "X-Content-Type-Options"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": -5, "message": "x-content-type-options-not-implemented."}

    if value.strip().lower() == "nosniff":
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 0, "message": "x-content-type-options-nosniff."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": -5, "message": "x-content-type-options-header-invalid."}
