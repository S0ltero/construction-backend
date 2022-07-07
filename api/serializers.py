from rest_framework import serializers

from .models import (
    ParentCategory, Category, SubCategory,
    Element, ElementDocument, Construction, 
    ConstructionElement, ConstructionDocument,
    Project, ProjectStage, 
    ProjectConstruction, ProjectConstructionDocument,
    ProjectElement, ProjectElementDocument,
    Template, TemplateStage, TemplateConstruction,
    TemplateElement,
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
        elements = validated_data.pop("elements", [])
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
    client = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class ProjectCreateSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(
        read_only=False,
        queryset=Template.objects.all(),
        required=False
    )

    class Meta:
        model = Project
        fields = "__all__"

    def create(self, validated_data):
        template = validated_data.pop("template", None)
        project = super().create(validated_data)

        bulk_insert_stages = []
        bulk_insert_constructions = []
        bulk_insert_elements = []

        if template:
            data = TemplateDetailSerilaizer(template).data
            stages = data.pop("stages", [])
            for stage in stages:
                del stage["id"]
                del stage["template"]
                contstructions = stage.pop("constructions", [])
                stage = ProjectStage(**stage, project=project)
                bulk_insert_stages.append(stage)

                for construction in contstructions:
                    elements = construction.pop("elements", [])
                    construction = ProjectConstruction(**construction, stage=stage)
                    bulk_insert_constructions.append(construction)

                    for element in elements:
                        element_instance = Element.objects.get(pk=element.pop("element"))
                        bulk_insert_elements.append(ProjectElement(
                            title=element["title"],
                            count=element["count"],
                            consumption=element["consumption"],
                            construction=construction,
                            element=element_instance
                        ))

            ProjectStage.objects.bulk_create(bulk_insert_stages)
            ProjectConstruction.objects.bulk_create(bulk_insert_constructions)
            ProjectElement.objects.bulk_create(bulk_insert_elements)

        return project


class ProjectElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectElement
        exclude = ("construction",)
        extra_kwargs = {"construction": {"required": False}}


class ProjectConstructionSerializer(serializers.ModelSerializer):
    elements = ProjectElementSerializer(many=True, read_only=False)

    class Meta:
        model = ProjectConstruction
        fields = ("id", "title", "count", "measure", "elements", "construction")
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
        bulk_insert_constructions_docs = []

        bulk_insert_elements = []
        bulk_insert_elements_docs = []

        for construction in constructions:
            elements = construction.pop("elements", [])

            template_construction = construction.pop("construction", None)
            construction = ProjectConstruction(
                **construction,
                stage=instance,
                construction=template_construction
            )

            # Reassign construction documents to project construction
            if template_construction:
                for document in template_construction.documents.all():
                    bulk_insert_constructions_docs.append(
                        ProjectConstructionDocument(construction=construction, file=document.file)
                    )

            bulk_insert_constructions.append(construction)
            for element in elements:
                template_element = element.pop("element", None)
                element = ProjectElement(
                    **element,
                    construction=construction,
                )

                if template_element:
                    element.element = template_element

                    # Add price and cost to element from already used element
                    if stage.used_elements.get(str(template_element.id)):
                        element.price = stage.used_elements[str(template_element.id)]["price"]
                        element.cost = stage.used_elements[str(template_element.id)]["cost"]
                    else:
                        stage.used_elements[str(template_element.id)] = {
                            "price": element.price,
                            "cost": element.cost,
                        }

                    # Reassign element documents to project element
                    for document in template_element.documents.all():
                        bulk_insert_elements_docs.append(
                            ProjectElementDocument(element=element, file=document.file)
                        )

                bulk_insert_elements.append(element)

        ProjectConstruction.objects.bulk_create(bulk_insert_constructions)
        ProjectConstructionDocument.objects.bulk_create(bulk_insert_constructions_docs)

        ProjectElement.objects.bulk_create(bulk_insert_elements)
        ProjectElementDocument.objects.bulk_create(bulk_insert_elements_docs)

        stage.save()
        serializer = ProjectStageSerializer(stage)
        return serializer.data


class ProjectDetailSerializer(ProjectSerializer):
    stages = ProjectStageSerializer(many=True)
    documents = serializers.SlugRelatedField(slug_field="file_url", many=True, read_only=True)


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = "__all__"


class TemplateElementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectElement
        exclude = ("construction",)
        extra_kwargs = {"construction": {"required": False}}


class TemplateConstructionSerializer(serializers.ModelSerializer):
    elements = TemplateElementSerializer(many=True, read_only=False)

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
                    TemplateElement(
                        **element, construction=construction
                    )
                )

        TemplateConstruction.objects.bulk_create(bulk_insert_constructions)
        TemplateElement.objects.bulk_create(bulk_insert_elements)

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
