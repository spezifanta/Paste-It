from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.context_processors import csrf
from paste.form import PasteForm
from paste.models import Paste

from pygments import highlight
from pygments import lexers
from pygments.formatters import HtmlFormatter

def add(request):
    if request.method == 'POST':
        form = PasteForm(request.POST)
        if form.is_valid():
            form.save()
            paste = Paste.objects.latest()
            return redirect('/%s' % paste.pk)
    else:
        form = PasteForm()

    tpl_var = {'paste_form': form, 'title': 'Add'}
    tpl_var.update(csrf(request))
    return render_to_response('add.html', tpl_var)

def view(request, pk, output_type=None):
    paste = get_object_or_404(Paste, pk=pk)

    # Update view counter
    #paste.view += 1
    #paste.save(update=True)

    if output_type:
        response = HttpResponse(paste.content)
        response['Content-Type'] = 'text/plain; charset=utf-8' # Fix UTF-8

        if output_type == 'raw':
            return response
        elif output_type == 'download':
            # TODO: add download size and mimetype
            response['Content-Disposition'] = 'attachment; filename=%s.%s' % (paste.id, paste.language.ext)
            return response
        else:
            return redirect('/%s' % paste.pk)
    else:
        lexer = lexers.get_lexer_by_name(paste.language.short)
        new_content = map(lambda line: highlight(line,
                                                 lexer,
                                                 HtmlFormatter(nowrap=True)),
                          paste.content.split('\n'))

        form = PasteForm(instance=paste)
        tpl_var = {
            'paste_form': form,
            'paste_id': paste.id,
            'title': '%s: %s' % (paste.language.name, paste.get_title()),
            'content': new_content,
        }
        tpl_var.update(csrf(request))
        return render_to_response('add.html', tpl_var)
