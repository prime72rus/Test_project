from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from network.permissions import IsActiveEmployee
from network.serializers import NetworkNodeSerializer

from .models import NetworkNode


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related("contact", "supplier")
    serializer_class = NetworkNodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveEmployee]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["contact__country"]
    search_fields = [
        "name",
        "contact__email",
        "contact__country",
        "contact__city",
    ]
    ordering_fields = ["name", "created_at", "debt"]

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.query_params.get("country")
        if country:
            queryset = queryset.filter(contact__country__iexact=country)
        return queryset

    def perform_update(self, serializer):
        if "debt" in serializer.validated_data:
            raise PermissionDenied("Изменение задолженности запрещено")
