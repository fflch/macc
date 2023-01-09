from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from django_countries.fields import CountryField
from datetime import date, timedelta

from account.models import Profile, User


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        label=gettext_lazy('Data de nascimento'),
        initial=date.today() - timedelta(7300),
        widget=forms.widgets.DateInput({
            'type': 'date'
        })
        # widget=forms.SelectDateWidget(
        #     years=range(date.today().year - 1, date.today().year - 150, -1)
        # )
    )
    country = CountryField().formfield(label=gettext_lazy('País'), initial='BR')
    gender = forms.ChoiceField(
        label=gettext_lazy('Gênero'),
        choices=Profile.CHOICES['gender'],
        required=False,
    )
    occupation = forms.CharField(label=gettext_lazy('Profissão'))
    education_institution = forms.BooleanField(
        label=gettext_lazy(
            'Possui vínculo com alguma instituição educacional?'),
        required=False,
    )

    class Meta:
        model = Profile
        fields = ['birth_date', 'country', 'gender', 'occupation',
                  'education_institution']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.label_suffix = '*' if field.required else ''

            match field_name:
                case 'education_institution':
                    field.widget.attrs.update({'class': 'form-check-input'})
                case _:
                    field.widget.attrs.update({'class': 'form-control'})


class UserRegistrationForm(UserCreationForm):
    consent = forms.BooleanField(
        label=gettext_lazy('Termo de compromisso'),
        error_messages={
            'consent': [gettext_lazy('Você deve aceitar o termo de compromisso')]
        },
    )
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'username',
                  'password1', 'password2', 'consent']

    def save(self, commit=True):
        user: User = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].label = gettext_lazy('Nome')
        self.fields['last_name'].label = gettext_lazy('Sobrenome')

        for field_name, field in self.fields.items():
            field.label_suffix = '*' if field.required else ''

            match field_name:
                case 'consent':
                    field.widget.attrs.update({'class': 'form-check-input'})
                case _:
                    field.widget.attrs.update({'class': 'form-control'})


class UserAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = '*' if field.required else ''
            field.widget.attrs.update({'class': 'form-control'})

    username = forms.CharField(
        label=gettext_lazy('Usuário ou e-mail'),
        widget=forms.TextInput({'placeholder': 'Usuário ou e-mail'})
    )

    password = forms.CharField(
        label=gettext_lazy('Senha'),
        widget=forms.PasswordInput({'placeholder': 'Senha'})
    )


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = '*' if field.required else ''
            field.widget.attrs.update({'class': 'form-control'})


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=gettext_lazy('E-mail'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = '*' if field.required else ''
            field.widget.attrs.update({'class': 'form-control'})
