from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Parcel
from .serializers import (
    ParcelInboundSerializer,
    ParcelSerializer,
    PickupCodeSerializer,
    PickupExceptionSerializer,
)
from .services import inbound_parcel, open_by_pickup_code, record_pickup_exception


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.select_related("locker_cell").all()
    serializer_class = ParcelSerializer

    @action(detail=False, methods=["post"])
    def inbound(self, request):
        serializer = ParcelInboundSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parcel = inbound_parcel(serializer.validated_data)
        return Response(ParcelSerializer(parcel).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def open(self, request):
        serializer = PickupCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        operator = serializer.validated_data.get("operator", "系统")
        parcel = open_by_pickup_code(serializer.validated_data["pickup_code"], operator=operator)
        if not parcel:
            return Response(
                {"success": False, "message": "取件码无效或快件不可取。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "success": True,
                "message": f"柜格 {parcel.locker_cell.code} 已开箱。",
                "parcel": ParcelSerializer(parcel).data,
            }
        )

    @action(detail=False, methods=["post"])
    def report_exception(self, request):
        serializer = PickupExceptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exception = record_pickup_exception(**serializer.validated_data)
        return Response(
            {
                "success": True,
                "message": "异常已记录。",
                "id": exception.id,
            },
            status=status.HTTP_201_CREATED,
        )
