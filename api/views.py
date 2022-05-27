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
