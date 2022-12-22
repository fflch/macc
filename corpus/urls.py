from django.urls import path

from .views import index, show, search

app_name = 'corpus'

urlpatterns = [
    path('works/', index, name='index'),
    path('works/<int:pk>', show, name='show'),
    path('search/', search, name='search'),
]
