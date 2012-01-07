from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from paste.models import Paste, Language

@csrf_exempt 
def add(request):    
    if request.method == 'POST':
        language = request.POST['language']
        content = request.POST['content']

        try:
            lang = Language.objects.get(pk=language)
        except:
            lang = Language.objects.get(pk='txt')
   
        paste = Paste(content=content, language=lang)
        paste.save()
        paste = Paste.objects.latest()
        return HttpResponse(paste.pk, content_type='text/plain')
    else:
        return redirect('/api')

def list(request):
    output = ''.join('%s;%s\n' % (lang.ext, lang.name) for lang in Language.objects.all())
    return HttpResponse(output, content_type='text/plain')
