def check(headers, context):
    name = "HTTP -> HTTPS Redirect"
    initial = context.get("initial_url", "")
    final = context.get("final_url", "")
    chain = context.get("redirect_chain") or []

    if initial.startswith("https://"):
        return {"header_name": name, "status": "Present", "header_value": final,
                "points": 10, "message": "Initial request was already HTTPS."}

    if initial.startswith("http://") and final.startswith("https://"):
        if chain and chain[0].startswith("https://"):
            return {"header_name": name, "status": "Present", "header_value": final,
                    "points": 10, "message": "HTTP redirected directly to HTTPS."}
        return {"header_name": name, "status": "Present", "header_value": final,
                "points": 7, "message": "HTTP eventually redirected to HTTPS (not on first hop)."}

    return {"header_name": name, "status": "Missing", "header_value": final or initial,
            "points": 0, "message": "Site does not redirect HTTP to HTTPS."}
