from django.urls import re_path

from .views import show

app_name = 'catalogue'

urlpatterns = [
    re_path(r'(?P<code>(RO|CL)[0-9]{2})', show, name='show'),
]
