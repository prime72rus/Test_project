from rest_framework import serializers

from network.models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(
        source="supplier.name", read_only=True
    )

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ["created_at", "level"]

    def validate(self, data):
        supplier = data.get("supplier")
        node_type = data.get("node_type")

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

        return data
