from . import hsts, csp, x_frame_options, x_content_type_options, \
    referrer_policy, permissions_policy, coop, coep, corp, \
    set_cookie, https_redirect

ALL_RULES = [
    hsts.check,
    csp.check,
    x_frame_options.check,
    x_content_type_options.check,
    referrer_policy.check,
    permissions_policy.check,
    coop.check,
    coep.check,
    corp.check,
    set_cookie.check,
    https_redirect.check,
]
