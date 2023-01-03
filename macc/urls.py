"""macc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('account/', include('account.urls', namespace='account')),
    path('', include('page.urls', namespace='page')),
    path('corpus/', include('corpus.urls', namespace='corpus')),
    path('catalogue/', include('catalogue.urls', namespace='catalogue')),
)


if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'static/(?P<path>.*)$', serve, {
            'document_root': settings.STATIC_ROOT
        })
    ]
