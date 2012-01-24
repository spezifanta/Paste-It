from django.contrib import admin
from paste.models import Paste, Language


class PasteAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ['language', 'get_title', 'views', 'created']

admin.site.register(Paste, PasteAdmin)
admin.site.register(Language)

