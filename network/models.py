from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Contact(models.Model):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    def __str__(self):
        return self.email


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
    contact = models.OneToOneField(
        Contact, on_delete=models.CASCADE, verbose_name="Контакты"
    )
    products = models.ManyToManyField(Product)
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Поставщик",
    )
    debt = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal("0"))],
        verbose_name="Задолженность",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    level = models.IntegerField(
        default=0, editable=False, verbose_name="Уровень звена"
    )

    def save(self, *args, **kwargs):
        if self.supplier:
            self.level = self.supplier.level + 1
        else:
            self.level = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_node_type_display()})"
