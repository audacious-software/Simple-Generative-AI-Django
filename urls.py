# pylint: disable=line-too-long, no-name-in-module

import sys

from .views import models_json

if sys.version_info[0] > 2:
    from django.urls import re_path

    urlpatterns = [
        re_path(r'^models.json$', models_json, name='models_json'),
    ]
else:
    from django.conf.urls import url

    urlpatterns = [
        url(r'^models.json$', models_json, name='models_json'),
    ]
