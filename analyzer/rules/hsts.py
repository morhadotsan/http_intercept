def check(headers, context):
    name = "Strict-Transport-Security"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "HSTS header not set."}

    parts = [p.strip().lower() for p in value.split(";") if p.strip()]
    max_age = 0
    for p in parts:
        if p.startswith("max-age="):
            try:
                max_age = int(p.split("=", 1)[1])
            except ValueError:
                max_age = 0

    if max_age < 15552000:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": 5, "message": "max-age should be at least 15552000 (180 days)."}

    return {"header_name": name, "status": "Present", "header_value": value,
            "points": 15, "message": "HSTS configured with sufficient max-age."}
