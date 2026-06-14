from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import PickupException, ShiftHandover
from .serializers import (
    PickupExceptionSerializer,
    ShiftHandoverCreateSerializer,
    ShiftHandoverSerializer,
    ShiftStatsSerializer,
)
from .services import calculate_shift_stats, create_shift_handover


class ShiftHandoverViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShiftHandover.objects.all()
    serializer_class = ShiftHandoverSerializer

    def create(self, request, *args, **kwargs):
        serializer = ShiftHandoverCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        handover = create_shift_handover(serializer.validated_data)
        return Response(ShiftHandoverSerializer(handover).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        courier_name = request.query_params.get("courier_name")
        shift_start = request.query_params.get("shift_start")
        shift_end = request.query_params.get("shift_end")

        if not all([courier_name, shift_start, shift_end]):
            return Response(
                {"detail": "缺少必要参数: courier_name, shift_start, shift_end"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from django.utils.dateparse import parse_datetime

        start_dt = parse_datetime(shift_start)
        end_dt = parse_datetime(shift_end)
        if not start_dt or not end_dt:
            return Response(
                {"detail": "时间格式错误，请使用 ISO 格式。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        stats = calculate_shift_stats(courier_name, start_dt, end_dt)
        serializer = ShiftStatsSerializer(stats)
        return Response(serializer.data)


class PickupExceptionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PickupException.objects.all()
    serializer_class = PickupExceptionSerializer
