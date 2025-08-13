# pylint: disable=line-too-long, no-name-in-module

import sys

from django.contrib import admin
from django.urls import path

admin.autodiscover()
admin.site.enable_nav_sidebar = False

if sys.version_info[0] > 2:
    from django.urls import include, re_path

    urlpatterns = [
        path('admin/', admin.site.urls),
        re_path('^accounts/', include('django.contrib.auth.urls')),
        re_path(r'^generative-ai/', include('simple_generative_ai.urls')),
    ]
else:
    from django.conf.urls import include, url

    urlpatterns = [
        path('admin/', admin.site.urls),
        url('^accounts/', include('django.contrib.auth.urls')),
        url(r'^generative-ai/', include('simple_generative_ai.urls')),
    ]
