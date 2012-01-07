from django.shortcuts import render_to_response
from api.utils import get_latest_api, get_apis 

def index(requets):
    return render_to_response('%s/templates/index.html' % get_latest_api(), {'apis': get_apis()})
