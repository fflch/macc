from django.contrib import admin

from .models import Author, Translator, Work

admin.site.register(Author)
admin.site.register(Translator)
admin.site.register(Work)
