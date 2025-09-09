from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата релиза")

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    NODE_TYPES = (
        ("factory", "Завод"),
        ("retail", "Розничная сеть"),
        ("entrepreneur", "Индивидуальный предприниматель"),
    )

    name = models.CharField(
        max_length=100, unique=True, verbose_name="Название звена"
    )
    node_type = models.CharField(
        max_length=20, choices=NODE_TYPES, verbose_name="Тип звена"
    )
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    products = models.ManyToManyField(Product)
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="suppliers",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Задолженность",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    level = models.IntegerField(
        default=0, editable=False, verbose_name="Уровень звена"
    )

    def clean(self):
        """
        Кастомная валидация бизнес-логики:
        - Только завод может быть на уровне 0 (без поставщика)
        - Завод не может иметь поставщика
        - Максимальный уровень — 2
        """
        super().clean()

        if not self.supplier and self.debt != Decimal("0.00"):
            raise ValidationError(
                "Без поставщика задолженность должна быть 0!")

        if self.node_type == "factory" and self.supplier:
            raise ValidationError("Завод не может иметь поставщика!")

        if not self.supplier and self.node_type != "factory":
            raise ValidationError(
                "Только завод может быть без поставщика (уровень 0)!")

        if self.supplier and self.supplier.level >= 2:
            raise ValidationError(
                "Максимальный уровень иерархии — 2. Нельзя добавлять поставщиков выше этого уровня.")

    def save(self, *args, **kwargs):
        if self.supplier:
            self.level = self.supplier.level + 1
        else:
            self.level = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_node_type_display()})"
