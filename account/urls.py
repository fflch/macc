from django.urls import path

from .views import (register,
                    login,
                    logout,
                    activate,
                    register_success,
                    profile,
                    change_password,
                    reset_password,
                    reset_password_confirm)

app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),
    path('register/success/', register_success, name='register-success'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name='profile'),
    path('profile/change-password/', change_password, name='change-password'),
    path('reset-password/', reset_password, name='reset-password'),
    path('reset-password/<uidb64>/<token>/',
         reset_password_confirm, name='reset-password-confirm'),
]
