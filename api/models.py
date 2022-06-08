from django.db import models


# Create your models here.
class ParentCategory(models.Model):
    """
    Родительская категория
    """
    class Type(models.TextChoices):
        CONSTRUCTION = "CONSTRUCTION", "Конструкция"
        ELEMENT = "ELEMENT", "Элемент"

    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    type = models.CharField(verbose_name="Тип", choices=Type.choices, max_length=30)

    class Meta:
        verbose_name = "Родительская категория"
        verbose_name_plural = "Родительские категории"

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    parent_category = models.ForeignKey(ParentCategory, verbose_name="Родительская категория", on_delete=models.CASCADE, related_name="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name="subcategories")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.title


class Element(models.Model):
    class Type(models.TextChoices):
        MATERIAL = "MATERIAL", "Материал"
        JOB = "JOB", "Работа"

    title = models.CharField(verbose_name="Название", max_length=60)
    parent_category = models.ForeignKey(ParentCategory, verbose_name="Родительская категория", on_delete=models.CASCADE, related_name="elements")
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="elements",
        null=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        on_delete=models.CASCADE,
        related_name="elements",
        null=True
    )
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    second_measure = models.CharField(verbose_name="Доп. ед. измерения", max_length=30)
    cost = models.PositiveIntegerField(verbose_name="Себестоимость", default=0)
    price = models.PositiveIntegerField(verbose_name="Цена", default=0)
    type = models.CharField(verbose_name="Тип", choices=Type.choices, max_length=30)
    dimension = models.CharField(verbose_name="Размер", max_length=60, blank=True)
    conversion_rate = models.PositiveIntegerField(verbose_name="Норма конвертации")

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"

    def __str__(self):
        return self.title


class ElementDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    element = models.ForeignKey(Element, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="documents")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class Construction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    parent_category = models.ForeignKey(ParentCategory, verbose_name="Родительская категория", on_delete=models.CASCADE, related_name="constructions")
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="constructions",
        null=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        on_delete=models.CASCADE,
        related_name="constructions",
        null=True
    )

    class Meta:
        verbose_name = "Конструкция"
        verbose_name_plural = "Конструкции"

    def __str__(self):
        return self.title


class ConstructionDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    construction = models.ForeignKey(Construction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="documents")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class ConstructionElement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    element = models.ForeignKey(Element, verbose_name="Элемент", on_delete=models.CASCADE)
    construction = models.ForeignKey(Construction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="elements")
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)

    class Meta:
        verbose_name = "Элемент конструкции"
        verbose_name_plural = "Элементы конструкции"

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=60)
    url = models.TextField(verbose_name="Ссылка")

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.name


class Project(models.Model):
    class Type(models.TextChoices):
        FINISH = "FINISH", "Закончен"
        WORK = "WORK", "В работе"
        NOT_START = "NOT_START", "Не начат"

    title = models.CharField(verbose_name="Название", max_length=60)
    client = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE, related_name="projects")
    description = models.TextField(verbose_name="Описание")
    author = models.CharField(verbose_name="Автор", max_length=60)
    status = models.CharField(verbose_name="Статус", max_length=30, choices=Type.choices)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.title


class ProjectDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=models.CASCADE, related_name="documents")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class ProjectStage(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    project = models.ForeignKey(Project, verbose_name="Проект", on_delete=models.CASCADE, related_name="stages")
    order = models.IntegerField(verbose_name="Порядковый номер")
    data = models.JSONField(default=dict, blank=True)
    used_elements = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Стадия проекта"
        verbose_name_plural = "Стадии проекта"

    def __str__(self):
        return self.title


class ProjectConstruction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    count = models.PositiveIntegerField(verbose_name="Номер проекта")
    stage = models.ForeignKey(ProjectStage, verbose_name="Стадия", on_delete=models.CASCADE, related_name="constructions")
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)

    class Meta:
        verbose_name = "Конструкция проекта"
        verbose_name_plural = "Конструкции проекта"

    def __str__(self):
        return self.title


class ProjectConstructionElement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    element = models.ForeignKey(Element, verbose_name="Элемент", on_delete=models.CASCADE)
    construction = models.ForeignKey(ProjectConstruction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="elements")
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)

    class Meta:
        verbose_name = "Элемент проекта"
        verbose_name_plural = "Элементы проекта"

    def __str__(self):
        return self.title


class Template(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateField(verbose_name="Дата создания", auto_now=True)

    class Meta:
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"

    def __str__(self):
        return self.title


class TemplateStage(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    template = models.ForeignKey(Template, verbose_name="Шаблон", on_delete=models.CASCADE, related_name="stages")
    order = models.IntegerField(verbose_name="Порядковый номер")

    class Meta:
        verbose_name = "Стадия шаблона"
        verbose_name_plural = "Стадии шаблона"

    def __str__(self):
        return self.title


class TemplateConstruction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    count = models.PositiveIntegerField(verbose_name="Количество")
    stage = models.ForeignKey(TemplateStage, verbose_name="Стадия", on_delete=models.CASCADE, related_name="constructions")
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)

    class Meta:
        verbose_name = "Конструкция шаблона"
        verbose_name_plural = "Конструкции шаблона"

    def __str__(self):
        return self.title


class TemplateConstructionElement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    element = models.ForeignKey(Element, verbose_name="Элемент", on_delete=models.CASCADE)
    construction = models.ForeignKey(TemplateConstruction, verbose_name="Конструкция", on_delete=models.CASCADE, related_name="elements")
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)

    class Meta:
        verbose_name = "Элемент шаблона"
        verbose_name_plural = "Элементы шаблона"

    def __str__(self):
        return self.title
