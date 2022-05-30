from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    Category, SubCategory,
    Element, ElementDocument,
    Construction, ConstructionDocument,
    Project, ProjectStage, ProjectDocument,
    Template, TemplateStage,
    Client,
)

from . serializers import (
    CategorySerializer, SubCategorySerializer, ElementSerializer,
    ConstructionSerializer, ProjectSerializer, ProjectStageSerializer,
    TemplateSerializer, TemplateStageSerializer, ClientSerializer
)


# Create your views here.
class CategoryViewSet(viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        # Получение списка категорий
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        # Создание категории
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubCategoryViewSet(viewsets.GenericViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def create(self, request):
        # Создание подкатегории
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ElementViewSet(viewsets.GenericViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

    def list(self, request):
        # Получение списка элементов
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Создание элемента
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        # Редактирование элемента
        element = self.get_object()
        serializer = self.serializer_class(element, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.update(element, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Удаление элемента
        element = self.get_object()
        element.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConstructionViewset(viewsets.GenericViewSet):
    queryset = Construction.objects.all()
    serializer_class = ConstructionSerializer

    def list(self, request):
        # Получение списка конструкций
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Создание конструкции
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        # Редактирование конструкции и обновление списка элементов конструкции
        construction = self.get_object()
        serializer = self.serializer_class(construction, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.update(construction, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Удаление конструкции
        construction = self.get_object()
        construction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectViewset(viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request):
        # Создание проекта
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        # Редактирование проекта
        project = self.get_object()
        serializer = self.serializer_class(project, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.update(project, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Удаление проекта
        project = self.get_object()
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=["post"], url_name="stages", url_path="stages", serializer_class=ProjectStageSerializer, queryset=ProjectStage.objects.all())
    def add_stages(self, request, pk=None):
        # Добавление этапа проекта
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["delete", "patch"], url_name="stages", url_path=r"stages/(?P<stage_id>[^/.]+)", serializer_class=ProjectStageSerializer)
    def edit_stages(self, request, pk=None, stage_id=None):
        if request.method == "DELETE":
            # Удаление этапа проекта
            project = self.get_object()
            stage = project.stages.get(id=stage_id)
            stage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == "PATCH":
            # Добавление конструкций к этапу проекта
            project = self.get_object()
            stage = project.stages.get(id=stage_id)
            serializer = self.serializer_class(stage, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=False):
                serializer.update(stage, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateViewset(viewsets.GenericViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def list(self, request):
        # Получение списка шаблонов
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Добавление шаблона
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        # Редактирование шаблона
        template = self.get_object()
        serializer = self.serializer_class(template, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=False):
            serializer.update(template, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Удаление шаблона
        template = self.get_object()
        template.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=True, methods=["post"], url_name="stages", url_path="stages", serializer_class=TemplateStageSerializer, queryset=TemplateStage.objects.all())
    def add_stages(self, request, pk=None):
        # Добавление этапа шаблона
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["delete", "patch"], url_name="stages", url_path=r"stages/(?P<stage_id>[^/.]+)", serializer_class=TemplateStageSerializer)
    def edit_stages(self, request, pk=None, stage_id=None):
        if request.method == "DELETE":
            # Удаление этапа шаблона
            template = self.get_object()
            stage = template.stages.get(id=stage_id)
            stage.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method == "PATCH":
            # Добавление конструкций к этапу шаблона
            template = self.get_object()
            stage = template.stages.get(id=stage_id)
            serializer = self.serializer_class(stage, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=False):
                serializer.update(stage, serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientViewSet(viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def list(self, request):
        # Получение списка клиентов
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        # Добавление клиента
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        # Удаление клиента
        client = self.get_object()
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
