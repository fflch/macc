from django import forms
from django.utils.translation import gettext_lazy


class SearchCorpusForm(forms.Form):
    CHOICES = {
        'language': [
            ('pt', gettext_lazy('Português')),
            ('en', gettext_lazy('Inglês')),
        ],
        'search_type': [
            ('broad', gettext_lazy('Busca ampla')),
            ('exact', gettext_lazy('Busca exata')),
            ('start', gettext_lazy('Início')),
            ('end', gettext_lazy('Final')),
        ]
    }

    query = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput({
            'plceholder': gettext_lazy('Pesquisar...')
        })
    )
    language = forms.MultipleChoiceField(
        label=gettext_lazy('Buscar em ...'),
        choices=CHOICES['language'],
        widget=forms.CheckboxSelectMultiple(),
    )
    search_type = forms.ChoiceField(
        label=gettext_lazy('Modo de busca'),
        choices=CHOICES['search_type'],
        widget=forms.RadioSelect()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = '*' if field.required else ''

        self.fields['query'].widget.attrs.update({'class': 'form-control'})
