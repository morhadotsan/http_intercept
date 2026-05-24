SAFE = {"no-referrer", "same-origin", "strict-origin", "strict-origin-when-cross-origin"}
UNSAFE = {"origin", "origin-when-cross-origin", "unsafe-url", "no-referrer-when-downgrade"}


def check(headers, context):
    name = "Referrer-Policy"
    value = headers.get(name)
    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 0, "message": "referrer-policy-not-implemented."}

    tokens = [t.strip().lower() for t in value.split(",") if t.strip()]
    if not tokens:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -5, "message": "referrer-policy-header-invalid: empty value."}

    effective = tokens[-1]

    if effective in SAFE:
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "referrer-policy-private."}

    if effective in UNSAFE:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -5, "message": "referrer-policy-unsafe."}

    return {"header_name": name, "status": "Misconfigured", "header_value": value,
            "points": -5, "message": "referrer-policy-header-invalid: value not recognized."}
