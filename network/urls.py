from django.urls import path, include
from rest_framework.routers import DefaultRouter
from network.views import NetworkNodeViewSet
from network.apps import NetworkConfig


app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r'network-nodes', NetworkNodeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]