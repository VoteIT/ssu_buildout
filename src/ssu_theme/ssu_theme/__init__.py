

def includeme(config):
    config.include('.fanstatic_lib')
    config.add_static_view('static_ssu_theme', 'static', cache_max_age=3600)
