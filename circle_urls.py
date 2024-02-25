from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

admin.autodiscover()
admin.site.enable_nav_sidebar = False

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^generative-ai/', include('simple_generative_ai.urls')),
]
