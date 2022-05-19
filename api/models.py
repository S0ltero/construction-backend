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
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="elemnts")
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    second_measure = models.CharField(verbose_name="Вторая единица измерения", max_length=30)
    cost = models.PositiveIntegerField(verbose_name="Цена", default=0)
    price = models.PositiveIntegerField(verbose_name="Сумма", default=0)
    type = models.CharField(verbose_name="Тип", choices=Type.choices, max_length=30)
    dimension = models.CharField(verbose_name="Размер", max_length=60, blank=True)
    conversion_rate = models.PositiveIntegerField(verbose_name="Коэффициент конверсии")


class Construction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="constructions")


class ConstructionDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    construction = models.ForeignKey(Construction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="documents")
