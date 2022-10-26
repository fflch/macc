from django.contrib import admin

from .models import Author, Collection, Translator, Work, Place, Publisher, Translation, OriginalFragment, TranslatedFragment

admin.site.register(Author)
admin.site.register(Translator)
admin.site.register(Work)
admin.site.register(Place)
admin.site.register(Publisher)
admin.site.register(Collection)
admin.site.register(Translation)
admin.site.register(OriginalFragment)
admin.site.register(TranslatedFragment)
