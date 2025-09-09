from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from network.permissions import IsActiveEmployee
from network.serializers import NetworkNodeSerializer, ProductSerializer

from network.models import NetworkNode, Product


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]

    def perform_update(self, serializer):
        if "debt" in serializer.validated_data:
            raise PermissionDenied("Изменение задолженности запрещено")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveEmployee]