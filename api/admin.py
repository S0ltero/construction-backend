from django.contrib import admin

import nested_admin

from .models import (
    ElementDocument, ConstructionDocument, ProjectDocument,
    Category, SubCategory, Element,
    Construction, ConstructionElement,
    Project, ProjectStage, ProjectConstruction,
    ProjectConstructionElement,
    Template, TemplateStage, TemplateConstruction,
    TemplateConstructionElement,
    Client
)


# Register your models here.
class ElementDocumentsInline(admin.StackedInline):
    model = ElementDocument
    extra = 0
    classes = ["collapse"]


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 0
    classes = ["collapse"]
