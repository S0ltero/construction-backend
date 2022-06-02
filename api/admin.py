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


class ElementInline(admin.StackedInline):
    model = Element
    extra = 0
    classes = ["collapse"]


class ConstructionDocumentInline(admin.StackedInline):
    model = ConstructionDocument
    extra = 0
    classes = ["collapse"]


class ConstructionElementInline(admin.StackedInline):
    model = ConstructionElement
    extra = 0
    classes = ["collapse"]


class ConstructionImline(admin.StackedInline):
    model = Construction
    extra = 0
    classes = ["collapse"]


class SubCategoryInline(admin.StackedInline):
    model = SubCategory
    extra = 0
    classes = ["collapse"]


class NestedProjectnDocumentsInline(nested_admin.NestedStackedInline):
    model = ProjectDocument
    extra = 0
    classes = ["collapse"]


class NestedProjectElementInline(nested_admin.NestedStackedInline):
    model = ProjectConstructionElement
    extra = 0
    classes = ["collapse"]


class NestedConstructionInline(nested_admin.NestedStackedInline):
    model = ProjectConstruction
    extra = 0
    classes = ["collapse"]
    inlines = (NestedProjectElementInline, )


class NestedProjectStageInline(nested_admin.NestedStackedInline):
    model = ProjectStage
    extra = 0
    classes = ["collapse"]
    inlines = (NestedConstructionInline, )


class NestedTemplateElementInline(nested_admin.NestedStackedInline):
    model = TemplateConstructionElement
    extra = 0
    classes = ["collapse"]


class NestedTemplateConstructionInline(nested_admin.NestedStackedInline):
    model = TemplateConstruction
    extra = 0
    classes = ["collapse"]
    inlines = (NestedTemplateElementInline, )


class NestedTemplateStageInline(nested_admin.NestedStackedInline):
    model = TemplateStage
    extra = 0
    classes = ["collapse"]
    inlines = (NestedTemplateConstructionInline, )
