from rest_framework import serializers

from .models import (
    ParentCategory, Category, SubCategory,
    Element, Construction, ConstructionElement,
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


class ParentCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = ParentCategory
        fields = "__all__"


class ElementSerializer(serializers.ModelSerializer):
    documents = serializers.SlugRelatedField(slug_field="file_url", many=True, read_only=True)

    class Meta:
        model = Element
        fields = "__all__"


class ConstructionElementSerializer(serializers.ModelSerializer):
    measure = serializers.CharField(source="element.measure")
    price = serializers.IntegerField(source="element.price")
    cost = serializers.IntegerField(source="element.cost")

    class Meta:
        model = ConstructionElement
        fields = "__all__"


class ConstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Construction
        fields = "__all__"


class ConstructionDetailSerializer(serializers.ModelSerializer):
    elements = ConstructionElementSerializer(many=True, required=False)
    documents = serializers.SlugRelatedField(slug_field="file_url", many=True, read_only=True)

    class Meta:
        model = Construction
        fields = "__all__"

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


class ParentCategoryDetailSerializer(ParentCategorySerializer):
    elements = ElementSerializer(many=True)
    constructions = ConstructionSerializer(many=True)


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
    measure = serializers.CharField(source="element.measure")
    price = serializers.IntegerField(source="element.price")
    cost = serializers.IntegerField(source="element.cost")

    class Meta:
        model = ProjectConstructionElement
        exclude = ("construction",)
        extra_kwargs = {"construction": {"required": False}}


class ProjectConstructionSerializer(serializers.ModelSerializer):
    elements = ProjectConstructionElementSerializer(many=True, read_only=False)

    class Meta:
        model = ProjectConstruction
        fields = ("title", "count", "measure", "elements")
        extra_kwargs = {"stage": {"required": False}}


class ProjectStageSerializer(serializers.ModelSerializer):
    constructions = ProjectConstructionSerializer(many=True, read_only=False, required=False)

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
        serializer = ProjectStageSerializer(instance=stage, context={"no_data": True})

        data = serializer.data.copy()
        constructions = data["constructions"]

        # Process elements price and cost
        for const_index, construction in enumerate(constructions):
            elements = construction["elements"]
            for const_elem_index, const_element in enumerate(elements):
                element_id = const_element["element"]
                if stage.used_elements.get(str(element_id)):
                    # Add price and cost to element from already used element
                    elements[const_elem_index].update(stage.used_elements[str(element_id)])
                else:
                    # Add price and cost of element to used_elements data
                    stage.used_elements[str(element_id)] = {
                        "price": const_element["price"],
                        "cost": const_element["cost"],
                    }
            constructions[const_index]["elements"] = elements

        data["constructions"] = constructions

        stage.data = data
        stage.save()

        return data

    def to_representation(self, instance):
        if not instance.data or self.context.get("no_data"):
            return super().to_representation(instance)
        return instance.data


class ProjectDetailSerializer(ProjectSerializer):
    stages = ProjectStageSerializer(many=True)
    documents = serializers.SlugRelatedField(slug_field="file_url", many=True, read_only=True)


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class TemplateConstructionElementSerializer(serializers.ModelSerializer):
    measure = serializers.CharField(source="element.measure")
    price = serializers.IntegerField(source="element.price")
    cost = serializers.IntegerField(source="element.cost")

    class Meta:
        model = ProjectConstructionElement
        exclude = ("construction",)
        extra_kwargs = {"construction": {"required": False}}


class TemplateConstructionSerializer(serializers.ModelSerializer):
    elements = TemplateConstructionElementSerializer(many=True, read_only=False)

    class Meta:
        model = TemplateConstruction
        fields = ("title", "count", "measure", "elements")
        extra_kwargs = {"stage": {"required": False}}


class TemplateStageSerializer(serializers.ModelSerializer):
    constructions = TemplateConstructionSerializer(many=True, read_only=False, required=False)

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
