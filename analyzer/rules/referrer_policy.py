SAFE = {
    "no-referrer", "no-referrer-when-downgrade", "same-origin",
    "strict-origin", "strict-origin-when-cross-origin",
}


def check(headers, context):
    name = "Referrer-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "Referrer-Policy not set."}

    tokens = [t.strip().lower() for t in value.split(",")]
    if any(t in SAFE for t in tokens):
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "Referrer-Policy uses a safe value."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": 1, "message": "Referrer-Policy value is permissive."}
