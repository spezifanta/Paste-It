from django import forms
from django.forms import ModelForm
from paste.models import Paste, Language

class PasteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PasteForm, self).__init__(*args, **kwargs)
        self.fields['language'].label = 'Highlight as'
        self.fields['language'].empty_label = None
        self.fields['language'].choices = [('Default', [(lang.ext, lang) for lang in Language.objects.filter(favorite=True)])]
        self.fields['language'].choices.extend([('All', [(lang.ext, lang) for lang in Language.objects.all()])])

    class Meta:
        model = Paste
        fields = ['language', 'content']
