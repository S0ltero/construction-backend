from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter

from api.views import internal_media

router = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("docs/", TemplateView.as_view(template_name="elements.html")),
    re_path(r"^media/(?P<file>.*)/(?P<token>.*)$", internal_media, name="internal_media")
]
