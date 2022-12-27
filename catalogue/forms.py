from django import forms
from django.utils.translation import gettext_lazy

from corpus.models import Place


class SearchEnglishForm(forms.Form):
    year_from = forms.CharField(
        label=gettext_lazy('Ano'),
        required=False,
        widget=forms.NumberInput({'placeholder': gettext_lazy('De'), }),
    )
    year_until = forms.CharField(
        label=gettext_lazy('Ano'),
        required=False,
        widget=forms.NumberInput({'placeholder': gettext_lazy('Até'), }),
    )
    title_portuguese = forms.CharField(
        label='Título em português',
        required=False,
        widget=forms.TextInput()
    )
    title_english = forms.CharField(
        label='Título em inglês',
        required=False,
        widget=forms.TextInput()
    )
    gender = forms.MultipleChoiceField(
        label=gettext_lazy('Gênero literário'),
        required=False,
        choices=[
            ('RO', gettext_lazy('Romance')),
            ('NO', gettext_lazy('Novela')),
            ('CO', gettext_lazy('Conto')),
            ('CR', gettext_lazy('Crônica')),
        ],
        widget=forms.SelectMultiple(attrs={'size': 3})
    )
    country = forms.MultipleChoiceField(
        label=gettext_lazy('País'),
        required=False,
        choices=list(map(
            lambda country: (country[0], gettext_lazy(country[0])),
            Place
            .objects
            .distinct('country')
            .values_list('country'))),
        widget=forms.SelectMultiple(attrs={'size': 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class SearchPortugueseForm(forms.Form):
    title_portuguese = forms.CharField(
        label='Título em português',
        required=False,
        widget=forms.TextInput()
    )
    gender = forms.MultipleChoiceField(
        label=gettext_lazy('Gênero literário'),
        required=False,
        choices=[
            ('RO', gettext_lazy('Romance')),
            ('CL', gettext_lazy('Coletânea')),
            ('CR', gettext_lazy('Crônica')),
        ],
        widget=forms.SelectMultiple(attrs={'size': 3})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
