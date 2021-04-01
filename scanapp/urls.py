"""scanapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

#from django.urls import path
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, re_path
from apps.views import URLFormViewCelery, ScanResults, file_download

urlpatterns = [
    path('admin/', admin.site.urls),
    path('taejo_api/', URLFormViewCelery.as_view(), name='taejo_api'),
    re_path(r'^download/$', file_download),
    path('admin/', admin.site.urls),
    url(r'taejo_api_result/(?P<pk>[0-9]+)', ScanResults.as_view(), name='taejo_api_result')
]