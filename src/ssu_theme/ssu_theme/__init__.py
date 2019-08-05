

def includeme(config):
    config.include('.fanstatic_lib')
    config.include('.distrikt')
    config.include('.bifall_yrk')
    config.add_static_view('static_ssu_theme', 'static', cache_max_age=3600)
