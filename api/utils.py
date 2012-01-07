import os

def is_valid_api(dir):
    if dir.startswith('v') \
        and os.path.exists('api/%s/__init__.py' % dir) \
        and os.path.exists('api/%s/views.py' % dir) \
        and os.path.exists('api/%s/templates/index.html' % dir):
            return dir

def get_apis():
    apis = map(is_valid_api, os.listdir('api'))
    apis = filter(None, apis)
    apis.sort()
    return apis

def get_latest_api():
    return get_apis()[-1]
