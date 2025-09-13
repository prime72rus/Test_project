from rest_framework import serializers

from network.models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Product.
    """

    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели NetworkNode.
    """

    products_details = ProductSerializer(
        source="products", many=True, read_only=True
    )
    products = serializers.ListField(
        child=serializers.JSONField(),
        write_only=True,
        required=False,
    )
    supplier_name = serializers.CharField(
        source="supplier.name", read_only=True
    )

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "node_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "products",
            "products_details",
            "supplier",
            "supplier_name",
            "debt",
            "created_at",
            "level",
        ]
        read_only_fields = ["created_at", "level"]

    def create(self, validated_data):
        """
        Добавление продукта при создании звена сети.
        """

        products_data = validated_data.pop("products", [])
        instance = super().create(validated_data)

        self._process_products(instance, products_data)
        return instance

    def update(self, instance, validated_data):
        """
        Обновление продукта.
        """

        products_data = validated_data.pop("products", None)

        instance = super().update(instance, validated_data)

        if products_data is not None:
            instance.products.clear()
            self._process_products(instance, products_data)

        return instance

    def _process_products(self, instance, products_data):
        """
        Обработка продуктов: создание новых или привязка существующих.
        """

        for item in products_data:
            if isinstance(item, (int, str)) and str(item).isdigit():
                try:
                    product = Product.objects.get(id=int(item))
                    instance.products.add(product)
                except Product.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Продукт с ID {item} не существует"
                    )
            elif isinstance(item, dict):
                if "id" in item:
                    try:
                        product = Product.objects.get(id=item["id"])
                        instance.products.add(product)
                    except Product.DoesNotExist:
                        raise serializers.ValidationError(
                            f"Продукт с ID {item['id']} не существует"
                        )
                else:
                    product_serializer = ProductSerializer(data=item)
                    if product_serializer.is_valid():
                        product = product_serializer.save()
                        instance.products.add(product)
                    else:
                        raise serializers.ValidationError(
                            f"Ошибка валидации продукта: "
                            f"{product_serializer.errors}"
                        )
            else:
                raise serializers.ValidationError(
                    "Неверный формат данных продукта. "
                    "Ожидается ID (число) или объект с данными"
                )

    def validate_products(self, value):
        """
        Валидация данных продуктов.
        """

        for item in value:
            if isinstance(item, dict) and "id" in item and len(item) > 1:
                raise serializers.ValidationError(
                    "При указании ID продукта нельзя передавать другие поля"
                )
        return value

    def validate(self, data):
        """
        Валидация по поставщику.
        """

        instance = self.instance

        node_type = data.get("node_type", getattr(instance, "node_type", None))
        supplier = data.get("supplier", getattr(instance, "supplier", None))

        if instance is None:
            if node_type == "factory" and supplier:
                raise serializers.ValidationError(
                    "Завод не может иметь поставщика!"
                )
            if not supplier and node_type != "factory":
                raise serializers.ValidationError(
                    "Только завод может быть без поставщика (уровень 0)!"
                )
            if supplier and supplier.level >= 2:
                raise serializers.ValidationError(
                    "Максимальный уровень иерархии — 2."
                )

        else:
            if "node_type" in data or "supplier" in data:
                current_node_type = (
                    node_type if "node_type" in data else instance.node_type
                )
                current_supplier = (
                    supplier if "supplier" in data else instance.supplier
                )

                if current_node_type == "factory" and current_supplier:
                    raise serializers.ValidationError(
                        "Завод не может иметь поставщика!"
                    )
                if not current_supplier and current_node_type != "factory":
                    raise serializers.ValidationError(
                        "Только завод может быть без поставщика (уровень 0)!"
                    )
                if current_supplier and current_supplier.level >= 2:
                    raise serializers.ValidationError(
                        "Максимальный уровень иерархии — 2."
                    )

        return data

    def get_fields(self):
        """
        Определение заполнения полей "Тип звена", "Поставщик" при обновлении.
        """

        fields = super().get_fields()

        request_method = self.context.get("request", None)
        if request_method and request_method.method in ["PATCH", "PUT"]:
            fields["node_type"].required = False
            fields["supplier"].required = False

        return fields
