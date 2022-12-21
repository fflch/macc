from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserAuthenticationForm

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    form = UserRegistrationForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect(request.GET.get('next') or 'home')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    return render(request, 'account/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect(request.GET.get('next') or 'home')

    if request.POST:
        form = UserAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                auth.login(request, user)
                messages.success(
                    request,
                    f"Hello <b>{user.username}</b>! You have been logged in",
                    extra_tags='alert-autoclose')
                return redirect(request.GET.get('next') or 'home')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = UserAuthenticationForm()

    return render(request, 'account/login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logged out successfully!',
                  extra_tags='alert-autoclose')
    return redirect('home')
