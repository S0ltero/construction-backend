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


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = "__all__"


class ConstructionElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstructionElement
        fields = "__all__"


class ConstructionSerializer(serializers.ModelSerializer):
    elements = ConstructionElementSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Construction
        fields = ("id", "title", "measure", "category", "elements")
        extra_kwargs = {"elements": {"required": False}}


    def update(self, instance, validated_data):
        elements = validated_data.pop("elements")
        instance.title = validated_data.get("title", instance.title)
        instance.measure = validated_data.get("measure", instance.measure)
        instance.category = validated_data.get("category", instance.category)
        instance.save()

        bulk_create = []

        if elements:
            instance.elements.all().delete()

        for element in elements:
            bulk_create.append(ConstructionElement(construction_id=instance.id, **element))

        ConstructionElement.objects.bulk_create(bulk_create)
        return instance


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectConstructionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectConstruction
        fields = "__all__"


class ProjectStageSerializer(serializers.ModelSerializer):
    constructions = ProjectConstructionSerializers

    class Meta:
        model = ProjectStage
        fields = "__all__"

    def update(self, instance, validated_data):
        constructions = validated_data.pop("constructions")
        instance.title = validated_data.get("title", instance.title)
        instance.project = validated_data.get("project", instance.project)
        instance.order = validated_data.get("order", instance.order)
        instance.save()

        bulk_create = []

        if constructions:
            instance.constructions.all().delete()

        for construction in constructions:
            bulk_create.append(ProjectConstruction(project_id=instance.id, **construction))

        ProjectConstruction.objects.bulk_create(bulk_create)
        return instance


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"
