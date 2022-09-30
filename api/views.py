from itertools import groupby

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from rest_framework import permissions

from django.http import HttpResponse
from django.db.models import F

from openpyxl.writer.excel import save_virtual_workbook

from .models import (
    ParentCategory, Category, SubCategory,
    Element, ElementDocument,
    Construction, ConstructionDocument, ConstructionElement,
    Project, ProjectStage, ProjectConstruction,
    ProjectElement, ProjectDocument,
    Template, TemplateStage,
    TemplateConstruction, TemplateElement,
    Client,
)

from . serializers import (
    ParentCategorySerializer, ParentCategoryDetailSerializer,
    CategorySerializer, CategoryDetailSerializer,
    SubCategorySerializer, SubCategoryDetailSerializer,
    ElementSerializer, ConstructionDetailSerializer, ConstructionSerializer,
    ProjectSerializer, ProjectStageSerializer, ProjectDetailSerializer, ProjectCreateSerializer,
    TemplateSerializer, TemplateStageSerializer, TemplateDetailSerilaizer,
    ClientSerializer, ClientDetailSerializer
)

from .excel import foreman, purchaser, estimate


def get_object_fields(obj) -> dict:
    kwargs = {}
    for field in obj._meta.fields[1:]:
        kwargs[field.name] = getattr(obj, field.name)
    return kwargs


@api_view(("GET",))
@renderer_classes((JSONRenderer,))
def internal_media(request, file, token):
    has_access = False
    if request.user.is_authenticated:
        has_access = True
    try:
        Token.objects.get(key=token)
        has_access = True
    except Token.DoesNotExist:
        pass

    if has_access:
        response = HttpResponse()
        response["Content-Disposition"] = "attachment; filename=" + file
        # nginx uses this path to serve the file
        response["X-Accel-Redirect"] = "/internal/" + file # path to file
        return response
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


class ParentCategoryViewSet(viewsets.GenericViewSet):
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = ParentCategory.objects.all()
        type = self.request.query_params.get("type")
        if type:
            queryset = queryset.filter(type__in=[type, "NO"])

        return queryset

    def retrieve(self, request, pk=None):
        """
        Получение родительской категории по pk
        """
        category = self.get_object()
        serializer = ParentCategoryDetailSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Получение списка родительский категорий
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Создание родительской категории
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Частичное обновление родительской категории
        """
        parent_category = self.get_object()
        serializer = self.serializer_class(
            instance=parent_category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=False):
            serializer.update(parent_category, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Удаление родительской категории
        """
        parent_category = self.get_object()
        parent_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        """
        Получение категории по pk
        """
        category = self.get_object()
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Создание категории
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Частичное обновление категории
        """
        category = self.get_object()
        serializer = self.serializer_class(
            instance=category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=False):
            serializer.update(category, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Удаление категории по pk
        """
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryViewSet(viewsets.GenericViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, pk=None):
        """
        Получение подкатегории по pk
        """
        category = self.get_object()
        serializer = SubCategoryDetailSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Создание подкатегории
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Частичное обновление подкатегории
        """
        subcategory = self.get_object()
        serializer = self.serializer_class(
            instance=subcategory,
            data=request.data,
            partial=True
        )

        if serializer.is_valid(raise_exception=False):
            serializer.update(subcategory, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Удаление подкатегории по pk
        """
        subcategory = self.get_object()
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ElementViewSet(viewsets.GenericViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Element.objects.all()
        title = self.request.query_params.get("title")
        if title:
            queryset = queryset.filter(title__istartswith=title)[:5]

        return queryset

    def retrieve(self, request, pk=None):
        """
        Получение элемента по pk
        """
        element = self.get_object()
        serializer = self.serializer_class(element)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Получение списка элементов
        """
        elements = self.get_queryset()
        serializer = self.serializer_class(elements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Создание элемента
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()

            bulk_inserts = []
            for file in request.FILES.getlist("documents"):
                bulk_inserts.append(ElementDocument(file=file, element=serializer.instance))
            ElementDocument.objects.bulk_create(bulk_inserts)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Редактирование элемента
        """
        element = self.get_object()
        serializer = self.serializer_class(element, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            if request.data.get("documents_urls"):
                documents_del_urls = request.data.getlist("documents_urls")
                element.documents.filter(file__in=documents_del_urls).delete()

            bulk_inserts = []
            for file in request.FILES.getlist("documents"):
                bulk_inserts.append(ElementDocument(file=file, element=element))
            ElementDocument.objects.bulk_create(bulk_inserts)

            serializer.update(element, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Удаление элемента
        """
        element = self.get_object()
        element.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"], url_name="filter", url_path="filter")
    def filter(self, request):
        elements = self.get_queryset()
        elements = elements.annotate(subcategory_title=F("subcategory__title")).values()

        data = [
            {"title": key, "elements": list(result)} for key, result in
            groupby(elements, key=lambda item: item["subcategory_title"])
        ]

        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_name="clone", url_path="clone")
    def clone(self, request, pk=None):
        element = self.get_object()
        element.id = None
        element.save()

        serializer = self.serializer_class(element)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConstructionViewset(viewsets.GenericViewSet):
    queryset = Construction.objects.all()
    serializer_class = ConstructionDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Construction.objects.all()
        title = self.request.query_params.get("title")
        if title:
            queryset = queryset.filter(title__istartswith=title)[:5]

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ConstructionSerializer
        elif self.action == "retrieve":
            return ConstructionDetailSerializer
        else:
            return super().get_serializer_class()

    def retrieve(self, request, pk=None):
        construction = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(construction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Получение списка конструкций
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Создание конструкции
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()

            bulk_inserts = []
            for file in request.FILES.getlist("documents"):
                bulk_inserts.append(ConstructionDocument(file=file, construction=serializer.instance))
            ConstructionDocument.objects.bulk_create(bulk_inserts)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Редактирование конструкции и обновление списка элементов конструкции
        """
        construction = self.get_object()
        serializer = self.serializer_class(construction, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            if request.data.get("documents_urls"):
                documents_del_urls = request.data.getlist("documents_urls")
                construction.documents.filter(file__in=documents_del_urls).delete()

            bulk_inserts = []
            for file in request.FILES.getlist("documents"):
                bulk_inserts.append(ConstructionDocument(file=file, construction=construction))
            ConstructionDocument.objects.bulk_create(bulk_inserts)

            serializer.update(construction, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Удаление конструкции
        """
        construction = self.get_object()
        construction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_name="clone", url_path="clone")
    def clone(self, request, pk=None):
        construction: Construction = self.get_object()
        template_kwargs = get_object_fields(construction)
        new_construction = Construction(**template_kwargs)
        new_construction.save()

        bulk_create_elements = []

        for element in construction.elements.all():
            element_kwargs = get_object_fields(element)
            element_kwargs["construction"] = new_construction
            bulk_create_elements.append(ConstructionElement(**element_kwargs))

        ConstructionElement.objects.bulk_create(bulk_create_elements)

        return Response(status=status.HTTP_201_CREATED)


class ProjectViewset(viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectSerializer
        elif self.action == "retrieve":
            return ProjectDetailSerializer
        elif self.action == "create":
            return ProjectCreateSerializer
        else:
            return super().get_serializer_class()

    def retrieve(self, request, pk=None):
        """
        Получение проекта по pk
        """
        project = self.get_object()
        serializer = self.get_serializer_class()
        serializer = serializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Получение списка проектов
        """
        serializer = self.get_serializer_class()
        serializer = serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Создание проекта
        """
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()

            bulk_inserts = []
            for file in request.FILES.getlist("documents"):
                bulk_inserts.append(ProjectDocument(file=file, project=serializer.instance))
            ProjectDocument.objects.bulk_create(bulk_inserts)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Редактирование проекта
        """
        project = self.get_object()
        serializer = self.serializer_class(project, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            if request.data.get("documents_urls"):
                documents_del_urls = request.data.getlist("documents_urls")
                project.documents.filter(file__in=documents_del_urls).delete()

            bulk_inserts = []
            for file in request.FILES.getlist("documents"):
                bulk_inserts.append(ProjectDocument(file=file, project=project))
            ProjectDocument.objects.bulk_create(bulk_inserts)

            serializer.update(project, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Удаление проекта
        """
        project = self.get_object()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["get"],
        url_name="excel/foreman",
        url_path="excel/foreman",
        serializer_class=ProjectDetailSerializer,
        permission_classes=()
    )
    def excel_foreman(self, request, pk=None):
        project = self.get_object()
        data = ProjectDetailSerializer(project).data

        wb = foreman(data)

        response = HttpResponse(content=save_virtual_workbook(wb))
        response["Content-Disposition"] = "attachment; filename=foreman.xlsx"

        return response

    @action(
        detail=True,
        methods=["get"],
        url_name="excel/purchaser",
        url_path="excel/purchaser",
        serializer_class=ProjectDetailSerializer,
        permission_classes=()
    )
    def excel_purchaser(self, request, pk=None):
        project = self.get_object()
        data = ProjectDetailSerializer(project).data

        wb = purchaser(data)

        response = HttpResponse(content=save_virtual_workbook(wb))
        response["Content-Disposition"] = "attachment; filename=purchaser.xlsx"

        return response

    @action(
        detail=True,
        methods=["get"],
        url_name="excel/estimate",
        url_path="excel/estimate",
        serializer_class=ProjectDetailSerializer,
        permission_classes=()
    )
    def excel_estimate(self, request, pk=None):
        project = self.get_object()
        data = ProjectDetailSerializer(project).data

        wb = estimate(data)

        response = HttpResponse(content=save_virtual_workbook(wb))
        response["Content-Disposition"] = "attachment; filename=estimate.xlsx"

        return response

    @action(detail=True, methods=["get"], url_name="update-price", url_path="update-price", serializer_class=ProjectDetailSerializer)
    def update_price(self, request, pk=None):
        """
        Обновление цен проекта
        """
        project = self.get_object()
        stages = project.stages.all()
        for stage in stages:
            for construction in stage.constructions.all():
                for element in construction.elements.all():
                    element.update_price()

        serializer = self.serializer_class(project)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_name="stages",
        url_path="stages",
        serializer_class=ProjectStageSerializer
    )
    def add_stages(self, request, pk=None):
        """
        Добавление этапа проекта
        """
        project = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete", "patch"], url_name="stages", url_path=r"stages/(?P<stage_id>[^/.]+)", serializer_class=ProjectStageSerializer)
    def edit_stages(self, request, pk=None, stage_id=None):
        """
        DELETE: Удаление этапа проекта

        PATCH: Добавление конструкций к этапу проекта
        """
        if request.method == "DELETE":
            project = self.get_object()
            stage = project.stages.get(id=stage_id)
            stage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == "PATCH":
            project = self.get_object()
            stage = project.stages.get(id=stage_id)
            serializer = self.serializer_class(stage, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=False):
                data = serializer.update(stage, serializer.validated_data)
                return Response(data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_name="clone", url_path="clone")
    def clone(self, request, pk=None):
        project: Project = self.get_object()
        project_kwargs = get_object_fields(project)
        project = Project(**project_kwargs)
        project.save()

        bulk_create_stages = []
        bulk_create_constructions = []
        bulk_create_elements = []

        for stage in project.stages.all():
            stage_kwargs = get_object_fields(stage)
            stage_kwargs["template"] = project
            new_stage = ProjectStage(**stage_kwargs)
            bulk_create_stages.append(new_stage)

            construction: ProjectConstruction
            for construction in stage.constructions.all():
                construction_kwargs = get_object_fields(construction)
                construction_kwargs["stage"] = new_stage
                new_construction = ProjectConstruction(**construction_kwargs)
                bulk_create_constructions.append(new_construction)

                element: ProjectElement
                for element in construction.elements.all():
                    element_kwargs = get_object_fields(element)
                    element_kwargs["construction"] = new_construction
                    bulk_create_elements.append(ProjectElement(**element_kwargs))

        ProjectStage.objects.bulk_create(bulk_create_stages)
        ProjectConstruction.objects.bulk_create(bulk_create_constructions)
        ProjectElement.objects.bulk_create(bulk_create_elements)

        return Response(status=status.HTTP_201_CREATED)


class TemplateViewset(viewsets.GenericViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Template.objects.all()
        title = self.request.query_params.get("title")
        if title:
            queryset = queryset.filter(title__istartswith=title)[:5]

        return queryset

    def retrieve(self, request, pk=None):
        """
        Получение шаблона по pk
        """
        template = self.get_object()
        serializer = TemplateDetailSerilaizer(template)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Получение списка шаблонов
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Добавление шаблона
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """
        Редактирование шаблона
        """
        template = self.get_object()
        serializer = self.serializer_class(template, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.update(template, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Удаление шаблона
        """
        template = self.get_object()
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], url_name="stages", url_path="stages", serializer_class=TemplateStageSerializer, queryset=TemplateStage.objects.all())
    def add_stages(self, request, pk=None):
        """
        Добавление этапа шаблона
        """
        template = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save(template=template)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["delete", "patch"], url_name="stages", url_path=r"stages/(?P<stage_id>[^/.]+)", serializer_class=TemplateStageSerializer)
    def edit_stages(self, request, pk=None, stage_id=None):
        """
        DELETE: Удаление этапа шаблона

        PATCH: Добавление конструкций к этапу шаблона
        """
        if request.method == "DELETE":
            template = self.get_object()
            stage = template.stages.get(id=stage_id)
            stage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == "PATCH":
            template = self.get_object()
            stage = template.stages.get(id=stage_id)
            serializer = self.serializer_class(stage, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=False):
                serializer.update(stage, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_name="clone", url_path="clone")
    def clone(self, request, pk=None):
        template: Template = self.get_object()
        template_kwargs = get_object_fields(template)
        new_template = Template(**template_kwargs)
        new_template.save()

        bulk_create_stages = []
        bulk_create_constructions = []
        bulk_create_elements = []

        for stage in template.stages.all():
            stage_kwargs = get_object_fields(stage)
            stage_kwargs["template"] = new_template
            new_stage = TemplateStage(**stage_kwargs)
            bulk_create_stages.append(new_stage)

            construction: TemplateConstruction
            for construction in stage.constructions.all():
                construction_kwargs = get_object_fields(construction)
                construction_kwargs["stage"] = new_stage
                new_construction = TemplateConstruction(**construction_kwargs)
                bulk_create_constructions.append(new_construction)

                element: TemplateElement
                for element in construction.elements.all():
                    element_kwargs = get_object_fields(element)
                    element_kwargs["construction"] = new_construction
                    bulk_create_elements.append(TemplateElement(**element_kwargs))

        TemplateStage.objects.bulk_create(bulk_create_stages)
        TemplateConstruction.objects.bulk_create(bulk_create_constructions)
        TemplateElement.objects.bulk_create(bulk_create_elements)

        return Response(status=status.HTTP_201_CREATED)


class ClientViewSet(viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Client.objects.all()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__istartswith=name)[:5]

        return queryset

    def retrieve(self, request, pk=None):
        """
        Получение клиента по pk
        """
        client = self.get_object()
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        """
        Получение списка клиентов
        """
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """
        Добавление клиента
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Удаление клиента
        """
        client = self.get_object()
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
