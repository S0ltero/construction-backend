from django.db import models


# Create your models here.
class ParentCategory(models.Model):
    """
    Родительская категория
    """
    class Type(models.TextChoices):
        CONSTRUCTION = "CONSTRUCTION", "Конструкция"
        ELEMENT = "ELEMENT", "Элемент"
        NO = "NO", "Нет"

    title = models.CharField(verbose_name="Название", max_length=160)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    type = models.CharField(verbose_name="Тип", choices=Type.choices, max_length=30)

    class Meta:
        verbose_name = "Родительская категория"
        verbose_name_plural = "Родительские категории"

    def __str__(self):
        return self.title

    @classmethod
    def get_default_pk(cls):
        category, created = cls.objects.get_or_create(
            title="Без категории", defaults={
                "description": "Без категории",
                "type": cls.Type.NO
            }
        )
        return category.id


class Category(models.Model):
    title = models.CharField(verbose_name="Название", max_length=160)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    parent_category = models.ForeignKey(
        ParentCategory,
        verbose_name="Родительская категория",
        on_delete=models.CASCADE, 
        related_name="categories"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(verbose_name="Название", max_length=60)
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(verbose_name="Фото", blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.title


class BaseElement(models.Model):
    class Type(models.TextChoices):
        MATERIAL = "MATERIAL", "Материал"
        JOB = "JOB", "Работа"

    title = models.CharField(verbose_name="Название", max_length=160)
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    second_measure = models.CharField(verbose_name="Доп. ед. измерения", max_length=30)
    cost = models.FloatField(verbose_name="Себестоимость", default=0)
    price = models.FloatField(verbose_name="Цена", default=0)
    type = models.CharField(verbose_name="Тип", choices=Type.choices, max_length=30)
    dimension = models.CharField(verbose_name="Размер", max_length=60, blank=True)
    conversion_rate = models.FloatField(verbose_name="Норма конвертации")
    weight = models.FloatField(verbose_name="Вес")
    volume = models.FloatField(verbose_name="Объём")

    class Meta:
        abstract = True


class Element(BaseElement):
    parent_category = models.ForeignKey(
        ParentCategory,
        verbose_name="Родительская категория",
        on_delete=models.SET_DEFAULT,
        related_name="elements",
        default=ParentCategory.get_default_pk
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="elements",
        blank=True,
        null=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        on_delete=models.SET_NULL,
        related_name="elements",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Элемент"
        verbose_name_plural = "Элементы"

    def __str__(self):
        return self.title


class ElementDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    element = models.ForeignKey(
        Element,
        verbose_name="Конструкция",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class BaseConstruction(models.Model):
    title = models.CharField(verbose_name="Название", max_length=160)
    description = models.TextField(verbose_name="Описание", blank=True)
    measure = models.CharField(verbose_name="Единицы измерения", max_length=30)
    cost = models.FloatField(verbose_name="Себестоимость", default=0)
    price = models.FloatField(verbose_name="Цена", default=0)

    class Meta:
        abstract = True


class Construction(BaseConstruction):
    parent_category = models.ForeignKey(
        ParentCategory,
        verbose_name="Родительская категория",
        on_delete=models.SET_DEFAULT,
        related_name="constructions",
        default=ParentCategory.get_default_pk
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="constructions",
        blank=True,
        null=True
    )
    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name="Подкатегория",
        on_delete=models.SET_NULL,
        related_name="constructions",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Конструкция"
        verbose_name_plural = "Конструкции"

    def __str__(self):
        return self.title


class ConstructionDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    construction = models.ForeignKey(
        Construction,
        verbose_name="Конструкция",
        on_delete=models.CASCADE,
        related_name="documents"
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class ConstructionElement(models.Model):
    title = models.CharField(verbose_name="Название", max_length=160)
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)
    element = models.ForeignKey(
        Element,
        verbose_name="Элемент",
        on_delete=models.CASCADE
    )
    construction = models.ForeignKey(
        Construction,
        verbose_name="Конструкция",
        on_delete=models.CASCADE,
        related_name="elements",
    )

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

    title = models.CharField(verbose_name="Название", max_length=160)
    description = models.TextField(verbose_name="Описание")
    author = models.CharField(verbose_name="Автор", max_length=100)
    status = models.CharField(verbose_name="Статус", max_length=30, choices=Type.choices)
    created_at = models.DateField(verbose_name="Дата создания", auto_now=True)
    price = models.IntegerField(verbose_name="Стоимость", default=0)
    client = models.ForeignKey(
        Client,
        verbose_name="Клиент",
        on_delete=models.CASCADE,
        related_name="projects"
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.title


class ProjectDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    project = models.ForeignKey(
        Project,
        verbose_name="Проект",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class ProjectStage(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name="Проект",
        on_delete=models.CASCADE,
        related_name="stages",
    )
    title = models.CharField(verbose_name="Название", max_length=160)
    order = models.IntegerField(verbose_name="Порядковый номер")
    used_elements = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Стадия проекта"
        verbose_name_plural = "Стадии проекта"
        unique_together = ("project", "order")

    def __str__(self):
        return self.title


class ProjectConstruction(BaseConstruction):
    construction = models.ForeignKey(
        Construction,
        verbose_name="Конструкция",
        on_delete=models.SET_NULL,
        null=True,
    )
    count = models.FloatField(verbose_name="Количество")
    stage = models.ForeignKey(
        ProjectStage,
        verbose_name="Стадия",
        on_delete=models.CASCADE,
        related_name="constructions",
    )

    class Meta:
        verbose_name = "Конструкция проекта"
        verbose_name_plural = "Конструкции проекта"

    def __str__(self):
        return self.title


class ProjectConstructionDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    construction = models.ForeignKey(
        ProjectConstruction,
        verbose_name="Конструкция",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class ProjectElement(BaseElement):
    element = models.ForeignKey(
        Element,
        verbose_name="Элемент",
        on_delete=models.SET_NULL,
        null=True,
    )
    construction = models.ForeignKey(
        ProjectConstruction,
        verbose_name="Конструкция",
        on_delete=models.CASCADE,
        related_name="elements",
    )
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)
    count = models.FloatField(verbose_name="Количество", default=0)

    class Meta:
        verbose_name = "Элемент проекта"
        verbose_name_plural = "Элементы проекта"

    def __str__(self):
        return self.title

    def update_price(self):
        self.price = self.element.price
        self.cost = self.element.cost
        self.save()


class ProjectElementDocument(models.Model):
    file = models.FileField(verbose_name="Файл")
    element = models.ForeignKey(
        ProjectElement,
        verbose_name="Элемент",
        on_delete=models.CASCADE,
        related_name="documents",
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        return self.file.url


class Template(models.Model):
    title = models.CharField(verbose_name="Название", max_length=160)
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateField(verbose_name="Дата создания", auto_now=True)
    price = models.IntegerField(verbose_name="Стоимость", default=0)

    class Meta:
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"

    def __str__(self):
        return self.title


class TemplateStage(models.Model):
    title = models.CharField(verbose_name="Название", max_length=160)
    template = models.ForeignKey(
        Template,
        verbose_name="Шаблон",
        on_delete=models.CASCADE,
        related_name="stages",
    )
    order = models.IntegerField(verbose_name="Порядковый номер")

    class Meta:
        verbose_name = "Стадия шаблона"
        verbose_name_plural = "Стадии шаблона"

    def __str__(self):
        return self.title


class TemplateConstruction(BaseConstruction):
    construction = models.ForeignKey(
        Construction,
        verbose_name="Конструкция",
        on_delete=models.SET_NULL,
        null=True,
    )
    stage = models.ForeignKey(
        TemplateStage,
        verbose_name="Стадия",
        on_delete=models.CASCADE,
        related_name="constructions",
    )
    count = models.FloatField(verbose_name="Количество")

    class Meta:
        verbose_name = "Конструкция шаблона"
        verbose_name_plural = "Конструкции шаблона"

    def __str__(self):
        return self.title


class TemplateElement(BaseElement):
    element = models.ForeignKey(
        Element,
        verbose_name="Элемент",
        on_delete=models.SET_NULL,
        null=True,
    )
    construction = models.ForeignKey(
        TemplateConstruction,
        verbose_name="Конструкция",
        on_delete=models.CASCADE,
        related_name="elements",
    )
    consumption = models.FloatField(verbose_name="Норма расхода", default=0)
    count = models.FloatField(verbose_name="Количество", default=0)

    class Meta:
        verbose_name = "Элемент шаблона"
        verbose_name_plural = "Элементы шаблона"

    def __str__(self):
        return self.title
