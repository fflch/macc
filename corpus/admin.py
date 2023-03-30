from django.contrib import admin

from .models import Author, Collection, Translator, Work, Place, Publisher, Translation, OriginalFragment, TranslatedFragment


class TranslationAdmin(admin.ModelAdmin):
    list_display = ('work_code', 'work_title', 'code', 'title',)
    list_display_links = ('code',)
    # sortable_by = ('work_code', 'work_title', 'code', 'title',)

    list_select_related = ('work',)
    search_fields = ('work__title', 'title',)

    ordering = ('code',)

    @admin.display(ordering='work__code')
    def work_code(self, obj):
        return obj.work.code

    @admin.display(ordering='work__title')
    def work_title(self, obj):
        return obj.work.title


admin.site.register(Author)
admin.site.register(Translator)
admin.site.register(Work)
admin.site.register(Place)
admin.site.register(Publisher)
admin.site.register(Collection)
admin.site.register(Translation, TranslationAdmin)
admin.site.register(OriginalFragment)
admin.site.register(TranslatedFragment)
