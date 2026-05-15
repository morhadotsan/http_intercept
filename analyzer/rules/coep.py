VALID = {"require-corp", "credentialless"}


def check(headers, context):
    name = "Cross-Origin-Embedder-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "COEP not set."}

    if value.strip().lower() in VALID:
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "COEP set to a valid isolating value."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": 1, "message": "COEP value not recognized."}
