from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PickupExceptionViewSet, ShiftHandoverViewSet

router = DefaultRouter()
router.register(r"shifts", ShiftHandoverViewSet, basename="shift")
router.register(r"exceptions", PickupExceptionViewSet, basename="exception")

urlpatterns = [
    path("", include(router.urls)),
]
