from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied

from network.models import NetworkNode
from network.permissions import IsActiveEmployee
from network.serializers import NetworkNodeSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    Контроллер модели Звена сети.
    """
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveEmployee]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country"]

    def perform_update(self, serializer):
        """
        Ограничение доступа к изменению задолженности через API.
        """
        if "debt" in serializer.validated_data:
            raise PermissionDenied("Изменение задолженности запрещено")
        serializer.save()
