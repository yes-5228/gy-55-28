import random
from string import digits

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.handovers.models import PickupException
from apps.lockers.models import LockerCell
from apps.notifications.services import send_pickup_notification
from .models import Parcel


def generate_pickup_code():
    while True:
        code = "".join(random.choices(digits, k=6))
        if not Parcel.objects.filter(
            pickup_code=code,
            status__in=[Parcel.Status.STORED, Parcel.Status.RETURN_PENDING],
        ).exists():
            return code


@transaction.atomic
def inbound_parcel(validated_data):
    size = validated_data.pop("size", None)
    operator = validated_data.pop("operator", "系统")
    cells = LockerCell.objects.select_for_update().filter(status=LockerCell.Status.EMPTY)
    if size:
        cells = cells.filter(size=size)
    cell = cells.order_by("zone", "code").first()
    if not cell:
        raise ValidationError({"locker_cell": "没有可用柜格，请先释放或维护柜格。"})

    if Parcel.objects.filter(tracking_no=validated_data["tracking_no"]).exists():
        raise ValidationError({"tracking_no": "该运单号已经入库。"})

    parcel = Parcel.objects.create(
        **validated_data,
        locker_cell=cell,
        pickup_code=generate_pickup_code(),
        stored_by=operator,
    )
    cell.status = LockerCell.Status.OCCUPIED
    cell.save(update_fields=["status", "updated_at"])
    send_pickup_notification(parcel)
    return parcel


@transaction.atomic
def open_by_pickup_code(pickup_code, operator="系统"):
    parcel = (
        Parcel.objects.select_for_update()
        .select_related("locker_cell")
        .filter(pickup_code=pickup_code, status=Parcel.Status.STORED)
        .first()
    )
    if not parcel:
        return None

    now = timezone.now()
    parcel.status = Parcel.Status.PICKED_UP
    parcel.picked_up_at = now
    parcel.picked_up_by = operator
    parcel.save(update_fields=["status", "picked_up_at", "picked_up_by"])

    cell = parcel.locker_cell
    cell.status = LockerCell.Status.OPEN
    cell.last_opened_at = now
    cell.save(update_fields=["status", "last_opened_at", "updated_at"])
    return parcel


def record_pickup_exception(pickup_code, exception_type, operator, description="", parcel_tracking_no=""):
    return PickupException.objects.create(
        parcel_tracking_no=parcel_tracking_no,
        pickup_code=pickup_code,
        exception_type=exception_type,
        operator=operator,
        description=description,
    )
