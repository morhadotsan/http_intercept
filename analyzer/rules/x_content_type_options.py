def check(headers, context):
    name = "X-Content-Type-Options"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "X-Content-Type-Options not set."}

    if value.strip().lower() == "nosniff":
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "MIME sniffing disabled."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": 1, "message": "Value should be 'nosniff'."}
