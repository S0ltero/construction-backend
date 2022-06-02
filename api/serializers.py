from rest_framework import serializers

from .models import (
    Category, SubCategory, Element,
    Construction, ConstructionElement,
    Project, ProjectStage, ProjectConstruction,
    ProjectConstructionElement,
    Template, TemplateStage, TemplateConstruction,
    TemplateConstructionElement,
    Client
)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
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
    class Meta:
        model = Construction
        fields = "__all__"


class ConstructionDetailSerializer(serializers.ModelSerializer):
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


class CategoryDetailSerializer(CategorySerializer):
    elements = ElementSerializer(many=True)
    constructions = ConstructionSerializer(many=True)


class SubCategoryDetailSerializer(SubCategorySerializer):
    elements = ElementSerializer(many=True)
    constructions = ConstructionSerializer(many=True)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectConstructionElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectConstructionElement
        fields = "__all__"
        extra_kwargs = {"construction": {"required": False}}


class ProjectConstructionSerializer(serializers.ModelSerializer):
    elements = ProjectConstructionElementSerializer(many=True, read_only=False)

    class Meta:
        model = ProjectConstruction
        fields = ("id", "title", "count", "stage", "measure", "elements")
        extra_kwargs = {"stage": {"required": False}}


class ProjectStageSerializer(serializers.ModelSerializer):
    constructions = ProjectConstructionSerializer(many=True, read_only=False)

    class Meta:
        model = ProjectStage
        fields = ("id", "title", "project", "order", "constructions")

    def update(self, instance, validated_data):
        constructions = validated_data.pop("constructions", [])
        stage = super().update(instance, validated_data)

        if constructions:
            stage.constructions.all().delete()

        bulk_insert_constructions = []
        bulk_insert_elements = []

        for construction in constructions:
            elements = construction.pop("elements", [])
            construction = ProjectConstruction(**construction, stage=instance)
            bulk_insert_constructions.append(construction)
            for element in elements:
                bulk_insert_elements.append(
                    ProjectConstructionElement(
                        **element, construction=construction
                    )
                )

        ProjectConstruction.objects.bulk_create(bulk_insert_constructions)
        ProjectConstructionElement.objects.bulk_create(bulk_insert_elements)

        stage = ProjectStage.objects.get(id=instance.id)
        return ProjectStageSerializer(instance=stage).data


class ProjectDetailSerializer(ProjectSerializer):
    stages = ProjectStageSerializer(many=True)


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class TemplateConstructionElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectConstructionElement
        fields = "__all__"
        extra_kwargs = {"construction": {"required": False}}


class TemplateConstructionSerializer(serializers.ModelSerializer):
    elements = TemplateConstructionElementSerializer(many=True, read_only=False)

    class Meta:
        model = TemplateConstruction
        fields = ("id", "title", "count", "stage", "measure", "elements")
        extra_kwargs = {"stage": {"required": False}}


class TemplateStageSerializer(serializers.ModelSerializer):
    constructions = TemplateConstructionSerializer(many=True, read_only=False)

    class Meta:
        model = TemplateStage
        fields = ("id", "title", "template", "order", "constructions")

    def update(self, instance, validated_data):
        constructions = validated_data.pop("constructions", [])
        stage = super().update(instance, validated_data)

        if constructions:
            stage.constructions.all().delete()

        bulk_insert_constructions = []
        bulk_insert_elements = []

        for construction in constructions:
            elements = construction.pop("elements", [])
            construction = TemplateConstruction(**construction, stage=instance)
            bulk_insert_constructions.append(construction)
            for element in elements:
                bulk_insert_elements.append(
                    TemplateConstructionElement(
                        **element, construction=construction
                    )
                )

        TemplateConstruction.objects.bulk_create(bulk_insert_constructions)
        TemplateConstructionElement.objects.bulk_create(bulk_insert_elements)

        stage = TemplateStage.objects.get(id=instance.id)
        return TemplateStageSerializer(instance=stage).data


class TemplateDetailSerilaizer(TemplateSerializer):
    stages = TemplateStageSerializer(many=True)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class ClientDetailSerializer(ClientSerializer):
    projects = ProjectSerializer(many=True)
