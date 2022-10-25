from django.urls import path

from .views import index, show, search, detail

app_name = 'corpus'

urlpatterns = [
    path('works/', index, name='index'),
    path('works/<int:pk>', show, name='show'),
    path('works/<int:pk>/detail', detail, name='detail'),
    path('search/', search, name='search'),
]
