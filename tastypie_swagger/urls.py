try:
	from django.conf.urls import include, url
except ImportError:
	from django.conf.urls.defaults import url

from .views import SwaggerView

urlpatterns = [
    url(r'^$', SwaggerView.as_view(), name='index'),
]
