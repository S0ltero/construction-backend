from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("docs/", TemplateView.as_view(template_name="elements.html"))
]
