def check(headers, context):
    name = "Set-Cookie"
    cookies = context.get("set_cookies") or []
    if not cookies:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": 5, "message": "No cookies set (nothing to evaluate)."}

    issues = []
    for c in cookies:
        lc = c.lower()
        cookie_name = c.split("=", 1)[0].strip()
        flags = []
        if "secure" not in lc:
            flags.append("Secure")
        if "httponly" not in lc:
            flags.append("HttpOnly")
        if "samesite=" not in lc:
            flags.append("SameSite")
        if flags:
            issues.append(f"{cookie_name} missing {', '.join(flags)}")

    joined = "; ".join(cookies)
    if issues:
        return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                "points": 2, "message": "Cookies missing flags: " + " | ".join(issues)}

    return {"header_name": name, "status": "Present", "header_value": joined,
            "points": 10, "message": "All cookies set with Secure, HttpOnly, and SameSite."}
