from django.shortcuts import render_to_response, redirect, get_object_or_404

import os

def index(requets):
    current_dir = os.path.realpath(os.path.dirname(__file__))
    os.chdir(current_dir)
    apis = []
    for dir in os.listdir( os.path.realpath(os.path.dirname(__file__))):
        print dir
        if dir.startswith('v') \
        and os.path.isdir('%s' % dir) \
        and os.path.exists('%s/__init__.py' % dir) \
        and os.path.exists('%s/templates/index.html' % dir):
            apis.append(dir)

    apis.sort()
    current_api = apis[-1]
    
    return render_to_response('%s/templates/index.html' % current_api, {})
