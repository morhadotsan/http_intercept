SIX_MONTHS = 15768000
ONE_YEAR = 31536000


def _parse(value):
    parts = [p.strip() for p in value.split(";") if p.strip()]
    attrs = {}
    for p in parts:
        if "=" in p:
            k, v = p.split("=", 1)
            attrs[k.strip().lower()] = v.strip()
        else:
            attrs[p.strip().lower()] = True
    return attrs


def check(headers, context):
    name = "Strict-Transport-Security"
    final = (context.get("final_url") or "").lower()
    on_https = final.startswith("https://")

    value = headers.get(name)

    if not on_https:
        return {"header_name": name, "status": "Missing", "header_value": value,
                "points": -20, "message": "hsts-not-implemented-no-https: site not available over HTTPS."}

    if value is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": -20, "message": "hsts-not-implemented: header not implemented."}

    try:
        attrs = _parse(value)
        max_age = int(attrs.get("max-age", 0))
    except (ValueError, TypeError):
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -20, "message": "hsts-header-invalid: cannot parse max-age."}

    if max_age <= 0:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -20, "message": "hsts-header-invalid: max-age missing or zero."}

    preload_eligible = (
        attrs.get("preload") is True
        and attrs.get("includesubdomains") is True
        and max_age >= ONE_YEAR
    )

    if preload_eligible:
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 5, "message": "hsts-preloaded: meets preload requirements."}

    if max_age < SIX_MONTHS:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -10, "message": "hsts-implemented-max-age-less-than-six-months."}

    return {"header_name": name, "status": "Present", "header_value": value,
            "points": 0, "message": "hsts-implemented-max-age-at-least-six-months."}
