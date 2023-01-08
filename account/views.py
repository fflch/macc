from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy


from .forms import (ProfileForm,
                    UserRegistrationForm,
                    UserAuthenticationForm,
                    ChangePasswordForm,
                    PasswordResetForm)
from .tokens import password_token


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    user_form = UserRegistrationForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None)
    if request.POST:
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            activate_email(request, user)
            return redirect('account:register-success')
        else:
            for error in list(user_form.errors.values()):
                messages.error(request, error)
            for error in list(profile_form.errors.values()):
                messages.error(request, error)

    return render(request, 'account/registration.html',
                  {'user_form': user_form, 'profile_form': profile_form})


def activate_email(request, user):
    mail_subject = 'MACC - Confirme seu e-mail'
    message = render_to_string(
        'account/email/activation.html',
        {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': password_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject, message, to=[user.email])
    if email.send():
        messages.success(
            request,
            f'Caro <strong>{user}</strong>: '
            f'acesse seu e-mail <strong>{user.email}</strong> e '
            f'clique no link para ativar sua conta.<br>'
            f'Caso não encontre em sua caixa de entrada, '
            f'pedimos que <strong>verifique</strong> sua caixa de <em>spam</em>.')
    else:
        messages.error(
            request, f'Problem sending confirmation email to {user.email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = auth.get_user_model()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (ValueError, User.DoesNotExist):
        user = None

    if user and password_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('account:login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('page:home')


def register_success(request):
    if request.user.is_authenticated:
        return redirect('page:home')
    return render(request, 'account/register_success.html', {})


@login_required
def change_password(request):
    user = request.user

    if request.POST:
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                gettext_lazy('Senha alterada com sucesso! '
                             'Refaça seu login utilizando a nova senha.')
            )
            return redirect('account:login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = ChangePasswordForm(user)
    return render(request, 'account/change_password.html', {'form': form})


def reset_password(request):
    if request.user.is_authenticated:
        return redirect('page:home')

    if request.POST:
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            User = auth.get_user_model()
            user_email = form.cleaned_data['email']
            try:
                associated_user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                pass
            else:
                subject = "Password Reset request"
                message = render_to_string(
                    'account/email/reset_password.html',
                    {
                        'user': associated_user,
                        'domain': get_current_site(request).domain,
                        'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                        'token': password_token.make_token(associated_user),
                        "protocol": 'https' if request.is_secure() else 'http'
                    }
                )
                email = EmailMessage(subject, message, to=[
                                     associated_user.email])
                if email.send():
                    messages.success(request,
                                     """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered.
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address
                            you registered with, and check your spam folder.
                        </p>
                        """
                                     )
                else:
                    messages.error(
                        request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('page:home')

    form = PasswordResetForm()
    return render(request, 'account/reset_password.html', {"form": form})


def reset_password_confirm(request, uidb64, token):
    User = auth.get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (ValueError, User.DoesNotExist):
        user = None

    if user and password_token.check_token(user, token):
        if request.POST:
            form = ChangePasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request,
                    'Your password has been set. You may go ahead '
                    'and <b>log in</b> now.'
                )
                return redirect('pages:home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = ChangePasswordForm(user)
        return render(request, 'account/change_password.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(
        request, 'Something went wrong, redirecting back to Homepage')
    return redirect('page:home')


@login_required
def profile(request):
    return render(request, 'account/profile.html', {})


def login(request):
    if request.user.is_authenticated:
        return redirect('page:home')

    if request.POST:
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                auth.login(request, user)
                messages.success(
                    request,
                    gettext_lazy(
                        f'Sua conexão como <strong>{user.email}</strong> '
                        f'foi estabelecida. Clique <a href={reverse("account:logout")}>'
                        'aqui</a> para sair agora.'
                    ),
                    extra_tags='alert-autoclose')
                return redirect('page:home')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = UserAuthenticationForm()

    return render(request, 'account/login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, gettext_lazy('Desconectado!'),
                  extra_tags='alert-autoclose')
    return render(request, 'account/logout.html', {})
