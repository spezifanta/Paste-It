from django.shortcuts import render_to_response, redirect, get_object_or_404

def index(requets):
    return render_to_response('index.html', {})

