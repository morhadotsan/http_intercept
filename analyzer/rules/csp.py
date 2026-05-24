UNSAFE_TOKENS = ("'unsafe-inline'", "data:")
BROAD_SCHEMES = ("http:", "https:", "ftp:", "*")


def _parse(value):
    directives = {}
    for chunk in value.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split()
        if not parts:
            continue
        directives.setdefault(parts[0].lower(), []).extend(p for p in parts[1:])
    return directives


def _has_insecure_scheme(directives):
    for name, srcs in directives.items():
        if any(s.lower().startswith("http:") for s in srcs):
            return True
    return False


def _has_insecure_scheme_passive_only(directives):
    passive = {"img-src", "media-src"}
    found_in_passive = False
    for name, srcs in directives.items():
        if any(s.lower().startswith("http:") for s in srcs):
            if name in passive:
                found_in_passive = True
            else:
                return False
    return found_in_passive


def _script_src_unsafe(directives):
    script_like = directives.get("script-src") or directives.get("default-src") or []
    lowered = [s.lower() for s in script_like]
    if "'unsafe-inline'" in lowered or "data:" in lowered:
        return True
    if any(s in BROAD_SCHEMES for s in lowered):
        return True
    return False


def _object_src_unsafe(directives):
    obj = directives.get("object-src")
    if obj is None and "default-src" not in directives:
        return True
    if obj and any(s.lower() in BROAD_SCHEMES for s in obj):
        return True
    return False


def _style_src_unsafe_only(directives):
    style = directives.get("style-src") or []
    lowered = [s.lower() for s in style]
    if "'unsafe-inline'" in lowered or "data:" in lowered or any(s in BROAD_SCHEMES for s in lowered):
        script_unsafe = _script_src_unsafe(directives)
        return not script_unsafe
    return False


def check(headers, context):
    name = "Content-Security-Policy"
    value = headers.get(name)
    report_only = headers.get("Content-Security-Policy-Report-Only")

    if value is None and report_only is None:
        return {"header_name": name, "status": "Missing", "header_value": None,
                "points": -25, "message": "csp-not-implemented: header not implemented."}

    if value is None and report_only is not None:
        return {"header_name": name, "status": "Misconfigured", "header_value": report_only,
                "points": -25, "message": "csp-not-implemented-but-reporting-enabled."}

    try:
        directives = _parse(value)
    except Exception:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -25, "message": "csp-header-invalid: header cannot be parsed."}

    if not directives:
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -25, "message": "csp-header-invalid: no directives parsed."}

    if _script_src_unsafe(directives) or _object_src_unsafe(directives):
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -20, "message": "csp-implemented-with-unsafe-inline: unsafe sources in script-src/object-src."}

    if _has_insecure_scheme(directives):
        if _has_insecure_scheme_passive_only(directives):
            return {"header_name": name, "status": "Misconfigured", "header_value": value,
                    "points": -10, "message": "csp-implemented-with-insecure-scheme-in-passive-content-only."}
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -20, "message": "csp-implemented-with-insecure-scheme."}

    script_like = directives.get("script-src") or directives.get("default-src") or []
    if any(s.lower() == "'unsafe-eval'" for s in script_like):
        return {"header_name": name, "status": "Misconfigured", "header_value": value,
                "points": -10, "message": "csp-implemented-with-unsafe-eval."}

    if _style_src_unsafe_only(directives):
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 0, "message": "csp-implemented-with-unsafe-inline-in-style-src-only."}

    default_src = directives.get("default-src") or []
    form_action = directives.get("form-action") or []
    has_default_none = any(s.lower() == "'none'" for s in default_src)
    form_safe = any(s.lower() in ("'none'", "'self'") for s in form_action)
    if has_default_none and form_safe:
        return {"header_name": name, "status": "Present", "header_value": value,
                "points": 10, "message": "csp-implemented-with-no-unsafe-default-src-none."}

    return {"header_name": name, "status": "Present", "header_value": value,
            "points": 5, "message": "csp-implemented-with-no-unsafe."}
