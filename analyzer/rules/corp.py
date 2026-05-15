VALID = {"same-origin", "same-site", "cross-origin"}


def check(headers, context):
    name = "Cross-Origin-Resource-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "CORP not set."}

    if value.strip().lower() in VALID:
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "CORP set to a valid value."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": 1, "message": "CORP value not recognized."}
