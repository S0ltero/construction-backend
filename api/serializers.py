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
