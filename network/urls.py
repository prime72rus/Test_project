from django.urls import include, path
from rest_framework.routers import DefaultRouter

from network.apps import NetworkConfig
from network.views import NetworkNodeViewSet

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r"network-nodes", NetworkNodeViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
