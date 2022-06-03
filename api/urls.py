from rest_framework.routers import DefaultRouter

from .views import (
    ParentCategoryViewSet, SubCategoryViewSet, ElementViewSet,
    ConstructionViewset, ProjectViewset, TemplateViewset,
    ClientViewSet
)


app_name = 'api'

router = DefaultRouter()
router.register(r"parent-categories", ParentCategoryViewSet, basename="parent-categories")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"subcategories", SubCategoryViewSet, basename="subcategories")
router.register(r"elements", ElementViewSet, basename="elements")
router.register(r"constructions", ConstructionViewset, basename="constructions")
router.register(r"projects", ProjectViewset, basename="projects")
router.register(r"templates", TemplateViewset, basename="templates")
router.register(r"clients", ClientViewSet, basename="clients")

urlpatterns = [
] + router.urls
