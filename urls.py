from django.conf.urls import url

from .views import models_json

urlpatterns = [
    url(r'^models.json$', models_json, name='models_json'),
]
