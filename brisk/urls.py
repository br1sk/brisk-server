from django.conf.urls import include, url
from django.contrib import admin
from api.views import types, create, login

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^types/?', types),
    url(r'^radar/?', create),
    url(r'^login/?', login),
]
