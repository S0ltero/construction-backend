from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Category(models.Model):
    class Type(models.TextChoices):
        CONSTRUCTION = "Construction", "Конструкция"
        ELEMENT = "Element ", "Элемент"

    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    type = models.CharField(verbose_name="Тип", choices=Type.choices, max_length=30)


class SubCategory(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    parent_category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="subcategories")


class Element(models.Model):
    class Type(models.TextChoices):
        MATERIAL = "Material", "Материал"
        JOB = "Job ", "Работа"

    title = models.CharField(verbose_name="Название", max_length=60)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="elements")
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        on_delete=models.CASCADE,
        related_name="elements",
        null=True
    )
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    second_measure = models.CharField(verbose_name="Вторая единица измерения", max_length=30)
    cost = models.PositiveIntegerField(verbose_name="Цена", default=0)
    price = models.PositiveIntegerField(verbose_name="Сумма", default=0)
    type = models.CharField(verbose_name="Тип", choices=Type.choices, max_length=30)
    dimension = models.CharField(verbose_name="Размер", max_length=60, blank=True)
    conversion_rate = models.PositiveIntegerField(verbose_name="Коэффициент конверсии")


class ElementDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    Element = models.ForeignKey(Element, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="documents")


class Construction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="constructions")
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        on_delete=models.CASCADE,
        related_name="constructions",
        null=True
    )


class ConstructionDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    construction = models.ForeignKey(Construction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="documents")


class ConstructionElement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    element = models.ForeignKey(Element, verbose_name="Элемент", on_delete=models.CASCADE)
    construction = models.ForeignKey(Construction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="elements")
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)


class Client(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=60)
    url = models.TextField(verbose_name="Ссылка")


class Project(models.Model):
    class Type(models.TextChoices):
        FINISH = "Finish", "Закончен"
        WORK = "Work ", "В работе"
        NOT_START = "Not start ", "Не начат"

    title = models.CharField(verbose_name="Название", max_length=60)
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE, related_name="projects")
    description = models.TextField(verbose_name="Описание")
    author = models.CharField(verbose_name="Автор", max_length=60)
    status = models.CharField(verbose_name="Статус", max_length=30, choices=Type.choices)


class ProjectDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=models.CASCADE)


class ProjectStage(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=models.CASCADE, related_name="stages")
    order = models.IntegerField(verbose_name="Порядковый номер")


class ProjectConstruction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    count = models.PositiveIntegerField(verbose_name="Номер проекта")
    stage = models.ForeignKey(ProjectStage, verbose_name="Стадия", on_delete=models.CASCADE, related_name="constructions")
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)


class ProjectConstructionElement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    element = models.ForeignKey(Element, verbose_name="Элемент", on_delete=models.CASCADE)
    construction = models.ForeignKey(ProjectConstruction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="elements")
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)


class Template(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")


class TemplateStage(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    template = models.ForeignKey(Template, verbose_name="Шаблон", on_delete=models.CASCADE, related_name="stages")
    order = models.IntegerField(verbose_name="Порядковый номер")


class TemplateConstruction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    count = models.PositiveIntegerField(verbose_name="Номер проекта")
    stage = models.ForeignKey(TemplateStage, verbose_name="Стадия", on_delete=models.CASCADE, related_name="constructions")
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)


class TemplateConstructionElement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    element = models.ForeignKey(Element, verbose_name="Элемент", on_delete=models.CASCADE)
    construction = models.ForeignKey(TemplateConstruction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="elements")
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)


class User(AbstractUser):
    pass
