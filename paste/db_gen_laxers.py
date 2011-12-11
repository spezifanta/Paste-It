from pygments.lexers import get_all_lexers

from paste.models import Language

def view(request):
    laxers = get_all_lexers()
    for lax in laxers:
        print "Title", lax[0]
        title =lax[0]
        print "short", lax[1][0]
        short = lax[1][0]

        if lax[2]:
            print "ext", lax[2][0][2:]
            ext = lax[2][0][2:]
        else:
            ext = 'None'
        if lax[3]:
            print "mime", lax[3][0]
            mime = lax[3][0]
        else:
            mime = 'None'
        lang = Language()
        lang.name = title
        lang.short = short
        lang.ext = ext
        lang.mimetype = mime
        lang.save()
