VALID = {"same-origin", "same-origin-allow-popups", "same-site"}


def check(headers, context):
    name = "Cross-Origin-Opener-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "COOP not set."}

    if value.strip().lower() in VALID:
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "COOP set to a valid isolating value."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": 1, "message": "COOP value not recognized."}
