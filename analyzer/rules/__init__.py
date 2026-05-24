from . import (
    csp,
    set_cookie,
    cors,
    https_redirect,
    referrer_policy,
    hsts,
    subresource_integrity,
    x_content_type_options,
    x_frame_options,
    corp,
)

ALL_RULES = [
    csp.check,
    set_cookie.check,
    cors.check,
    https_redirect.check,
    referrer_policy.check,
    hsts.check,
    subresource_integrity.check,
    x_content_type_options.check,
    x_frame_options.check,
    corp.check,
]
