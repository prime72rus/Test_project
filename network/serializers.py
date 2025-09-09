from rest_framework import serializers

from network.models import Contact, NetworkNode, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(
        source="supplier.name", read_only=True
    )

    class Meta:
        model = NetworkNode
        fields = "__all__"
        read_only_fields = ["created_at", "level"]

    def create(self, validated_data):
        contact_data = validated_data.pop("contact")
        contact = Contact.objects.create(**contact_data)
        node = NetworkNode.objects.create(contact=contact, **validated_data)
        return node

    def update(self, instance, validated_data):
        contact_data = validated_data.pop("contact", None)
        if contact_data:
            contact_serializer = ContactSerializer(
                instance.contact, data=contact_data, partial=True
            )
            if contact_serializer.is_valid():
                contact_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
