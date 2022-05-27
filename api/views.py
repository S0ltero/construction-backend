from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    Category, SubCategory, Element,
    Construction, Project, ProjectStage,
    Template, TemplateStage, Client,
    ProjectDocument
)

from . serializers import (
    CategorySerializer, SubCategorySerializer, ElementSerializer,
    ConstructionSerializer, ProjectSerializer, ProjectStageSerializer,
    TemplateSerializer, TemplateStageSerializer, ClientSerializer,
    ProjectDocumentSerializers
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
