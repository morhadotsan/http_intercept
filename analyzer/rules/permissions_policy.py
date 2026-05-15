def check(headers, context):
    name = "Permissions-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "Permissions-Policy not set."}

    return {"header_name": name, "status": "Present", "header_value": value,
            "points": 5, "message": "Permissions-Policy is set."}
