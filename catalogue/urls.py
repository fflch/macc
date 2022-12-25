from django.urls import path, re_path

from .views import show, timeline, search_english, search_portuguese

app_name = 'catalogue'

urlpatterns = [
    path('timeline/', timeline, name='timeline'),
    path('search-english/', search_english, name='search-english'),
    path('search-portuguese/', search_portuguese, name='search-portuguese'),
    re_path(r'(?P<code>(RO|CL)[0-9]{2,3}(TR[0-9]{2})?)', show, name='show'),
]
