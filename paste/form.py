from django import forms
from django.forms import ModelForm
from paste.models import Paste, Language

class PasteForm(ModelForm):
    #id = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        super(PasteForm, self).__init__(*args, **kwargs)
        self.fields['language'].label = 'Highlight as'
        self.fields['language'].empty_label = None

    class Meta:
        model = Paste
        fields = ['language', 'content']
