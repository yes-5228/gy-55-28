from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.parcels.models import Parcel
from apps.returns.models import ReturnOrder
from .models import PickupException, ShiftHandover


def calculate_shift_stats(courier_name, shift_start, shift_end):
    inbound_count = Parcel.objects.filter(
        stored_by=courier_name,
        stored_at__gte=shift_start,
        stored_at__lt=shift_end,
    ).count()

    pickup_exception_count = PickupException.objects.filter(
        operator=courier_name,
        created_at__gte=shift_start,
        created_at__lt=shift_end,
    ).count()

    return_processed_count = ReturnOrder.objects.filter(
        operator=courier_name,
        completed_at__gte=shift_start,
        completed_at__lt=shift_end,
        status=ReturnOrder.Status.COMPLETED,
    ).count()

    return {
        "inbound_count": inbound_count,
        "pickup_exception_count": pickup_exception_count,
        "return_processed_count": return_processed_count,
    }


@transaction.atomic
def create_shift_handover(validated_data):
    courier_name = validated_data["courier_name"]
    shift_start = validated_data["shift_start"]
    shift_end = validated_data["shift_end"]

    if shift_start >= shift_end:
        raise ValidationError({"shift_end": "交班结束时间必须晚于开始时间。"})

    stats = calculate_shift_stats(courier_name, shift_start, shift_end)

    return ShiftHandover.objects.create(
        courier_name=courier_name,
        shift_start=shift_start,
        shift_end=shift_end,
        inbound_count=stats["inbound_count"],
        pickup_exception_count=stats["pickup_exception_count"],
        return_processed_count=stats["return_processed_count"],
        remark=validated_data.get("remark", ""),
        handed_by=validated_data["handed_by"],
        received_by=validated_data.get("received_by", ""),
    )
