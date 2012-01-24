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
        form = PasteForm(initial={'language': 'txt'}) # Default selection

    tpl_var = {'paste_form': form, 'title': 'Add'}
    tpl_var.update(csrf(request))
    return render_to_response('add.html', tpl_var)

def view(request, pk, output_type=None):
    paste = get_object_or_404(Paste, pk=pk)

    # TODO: fix
    # Update view counter
    #paste.views += 1
    #paste.save()

    if output_type:
        response = HttpResponse(paste.content)
        response['Content-Type'] = 'text/plain; charset=utf-8' # Fix UTF-8
        response['Content-Length'] = len(paste.content)

        if output_type == 'raw':
            return response

        elif output_type == 'download':
            response['Content-Disposition'] = 'attachment; filename=%s.%s' % (paste.id, paste.language.ext)

            if len(paste.language.mimetype) > 0:
                response['Content-Type'] = '%s; charset=utf-8' % paste.language.mimetype 

            return response
        # Invalid output types
        else:
            return redirect('/%s' % paste.pk)
    else:
        """ The normal HTML output """
        lines = paste.content.split('\n')

        # Syntax highlighter
        lexer = lexers.get_lexer_by_name(paste.language.short)
        lines = map(lambda line: highlight(line,
                                           lexer,
                                           HtmlFormatter(nowrap=True)), lines)

        # Fix line break
        lines = map(lambda line: line.replace('\n', '<br />'), lines)

        # Fix indentation
        new_content = map(lambda line: line.replace('  ', '&nbsp; '), lines)

        form = PasteForm(instance=paste)
        tpl_var = {
            'paste_form': form,
            'paste_id': paste.id,
            'title': '%s: %s' % (paste.language.name, paste.get_title()),
            'content': new_content,
        }
        tpl_var.update(csrf(request))
        return render_to_response('add.html', tpl_var)

def about(request):
    return render_to_response('about.html', {})
