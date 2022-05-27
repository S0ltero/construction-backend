from rest_framework import serializers

from .models import (
    Category, SubCategory, Element,
    Construction, Project, ProjectStage,
    Template, TemplateStage, Client,
    ConstructionElement,
    ProjectConstruction, TemplateConstruction,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
