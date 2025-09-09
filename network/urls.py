from django.urls import include, path
from rest_framework.routers import DefaultRouter

from network.apps import NetworkConfig
from network.views import NetworkNodeViewSet, ProductViewSet

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r"network-nodes", NetworkNodeViewSet)
router.register(r"network-nodes/products", ProductViewSet)
urlpatterns = [
    path("api/", include(router.urls)),
]
