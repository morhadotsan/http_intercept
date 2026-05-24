VALID_SAMESITE = {"strict", "lax", "none"}
STRICT_SAMESITE = {"strict", "lax"}
ANTI_CSRF_HINTS = ("csrf", "xsrf", "_token")


def _parse_cookie(raw):
    parts = [p.strip() for p in raw.split(";") if p.strip()]
    if not parts:
        return None
    nv = parts[0].split("=", 1)
    cookie_name = nv[0].strip()
    attrs = {}
    for p in parts[1:]:
        if "=" in p:
            k, v = p.split("=", 1)
            attrs[k.strip().lower()] = v.strip()
        else:
            attrs[p.strip().lower()] = True
    return cookie_name, attrs


def _is_session(attrs):
    return "max-age" not in attrs and "expires" not in attrs


def _is_anti_csrf(name):
    lower = name.lower()
    return any(h in lower for h in ANTI_CSRF_HINTS)


def check(headers, context):
    name = "Set-Cookie"
    cookies_raw = context.get("set_cookies") or []
    if not cookies_raw:
        return {"header_name": name, "status": "Present", "header_value": None,
                "points": 0, "message": "cookies-not-found: no cookies detected."}

    hsts = headers.get("Strict-Transport-Security")
    parsed = [c for c in (_parse_cookie(r) for r in cookies_raw) if c]
    joined = "; ".join(cookies_raw)

    session_no_secure = []
    session_no_httponly = []
    any_no_secure = []
    samesite_invalid = []
    anti_csrf_no_samesite = []
    all_samesite_strict = True

    for cname, attrs in parsed:
        secure = "secure" in attrs
        httponly = "httponly" in attrs
        samesite = attrs.get("samesite")
        samesite_lower = samesite.lower() if isinstance(samesite, str) else None
        session = _is_session(attrs)

        if not secure:
            any_no_secure.append(cname)
            if session:
                session_no_secure.append(cname)
        if session and not httponly:
            session_no_httponly.append(cname)
        if samesite_lower is not None and samesite_lower not in VALID_SAMESITE:
            samesite_invalid.append(cname)
        if samesite_lower not in STRICT_SAMESITE:
            all_samesite_strict = False
        if _is_anti_csrf(cname) and samesite_lower is None:
            anti_csrf_no_samesite.append(cname)

    if session_no_secure:
        return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                "points": -40, "message": f"cookies-session-without-secure-flag: {', '.join(session_no_secure)}."}

    if session_no_httponly:
        return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                "points": -30, "message": f"cookies-session-without-httponly-flag: {', '.join(session_no_httponly)}."}

    if samesite_invalid:
        return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                "points": -20, "message": f"cookies-samesite-flag-invalid: {', '.join(samesite_invalid)}."}

    if anti_csrf_no_samesite:
        return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                "points": -20, "message": f"cookies-anticsrf-without-samesite-flag: {', '.join(anti_csrf_no_samesite)}."}

    if any_no_secure:
        if hsts:
            session_under_hsts = [c for c, a in parsed if _is_session(a) and "secure" not in a]
            if session_under_hsts:
                return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                        "points": -10, "message": "cookies-session-without-secure-flag-but-protected-by-hsts."}
            return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                    "points": -5, "message": "cookies-without-secure-flag-but-protected-by-hsts."}
        return {"header_name": name, "status": "Misconfigured", "header_value": joined,
                "points": -20, "message": f"cookies-without-secure-flag: {', '.join(any_no_secure)}."}

    if all_samesite_strict:
        return {"header_name": name, "status": "Present", "header_value": joined,
                "points": 5, "message": "cookies-secure-with-httponly-sessions-and-samesite."}

    return {"header_name": name, "status": "Present", "header_value": joined,
            "points": 0, "message": "cookies-secure-with-httponly-sessions."}
