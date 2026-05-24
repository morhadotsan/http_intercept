import re
from urllib.parse import urlparse

SCRIPT_TAG_RE = re.compile(r"<script\b([^>]*)>", re.IGNORECASE)
ATTR_RE = re.compile(r'(\w[\w:-]*)\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s>]+))')


def _parse_attrs(raw):
    attrs = {}
    for m in ATTR_RE.finditer(raw):
        key = m.group(1).lower()
        val = m.group(3) or m.group(4) or m.group(5) or ""
        attrs[key] = val
    return attrs


def _is_external(src, final_host):
    if not src:
        return False
    if src.startswith("//"):
        return True
    parsed = urlparse(src)
    if not parsed.scheme:
        return False
    return parsed.hostname and parsed.hostname != final_host


def _is_insecure(src):
    if src.startswith("//"):
        return True
    if src.startswith("http://"):
        return True
    return False


def check(headers, context):
    name = "Subresource Integrity"
    content_type = (context.get("content_type") or "").lower()
    body = context.get("html_body") or ""
    final_url = context.get("final_url") or ""
    final_host = urlparse(final_url).hostname or ""

    if "html" not in content_type:
        return {"header_name": name, "status": "Present", "header_value": None,
                "points": 0, "message": "sri-not-implemented-response-not-html."}

    scripts = []
    for m in SCRIPT_TAG_RE.finditer(body):
        attrs = _parse_attrs(m.group(1))
        if "src" in attrs:
            scripts.append(attrs)

    if not scripts:
        return {"header_name": name, "status": "Present", "header_value": None,
                "points": 0, "message": "sri-not-implemented-but-no-scripts-loaded."}

    external = [s for s in scripts if _is_external(s["src"], final_host)]

    if not external:
        return {"header_name": name, "status": "Present", "header_value": None,
                "points": 0, "message": "sri-not-implemented-but-all-scripts-loaded-from-secure-origin."}

    insecure_external = [s for s in external if _is_insecure(s["src"])]
    with_integrity = [s for s in external if "integrity" in s]
    without_integrity = [s for s in external if "integrity" not in s]

    if insecure_external and without_integrity:
        return {"header_name": name, "status": "Misconfigured", "header_value": None,
                "points": -50, "message": "sri-not-implemented-and-external-scripts-not-loaded-securely."}

    if insecure_external and with_integrity:
        return {"header_name": name, "status": "Misconfigured", "header_value": None,
                "points": -20, "message": "sri-implemented-but-external-scripts-not-loaded-securely."}

    if without_integrity:
        return {"header_name": name, "status": "Misconfigured", "header_value": None,
                "points": -5, "message": "sri-not-implemented-but-external-scripts-loaded-securely."}

    return {"header_name": name, "status": "Present", "header_value": None,
            "points": 5, "message": "sri-implemented-and-external-scripts-loaded-securely."}
