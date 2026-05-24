def check(headers, context):
    name = "Access-Control-Allow-Origin"
    acao = headers.get(name)
    acac = (headers.get("Access-Control-Allow-Credentials") or "").strip().lower()

    if acao is None:
        return {"header_name": name, "status": "Present", "header_value": None,
                "points": 0, "message": "cross-origin-resource-sharing-not-implemented."}

    value = acao.strip()

    if value == "*" or (value == "null" and acac == "true"):
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -50, "message": "cross-origin-resource-sharing-implemented-with-universal-access."}

    if value == "*":
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 0, "message": "cross-origin-resource-sharing-implemented-with-public-access."}

    return {"header_name": name, "status": "Present", "header_value": value,
            "points": 0, "message": "cross-origin-resource-sharing-implemented-with-restricted-access."}
