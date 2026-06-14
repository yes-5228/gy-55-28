from django.contrib import admin

from .models import PickupException, ShiftHandover


@admin.register(ShiftHandover)
class ShiftHandoverAdmin(admin.ModelAdmin):
    list_display = [
        "courier_name",
        "shift_start",
        "shift_end",
        "inbound_count",
        "pickup_exception_count",
        "return_processed_count",
        "handed_by",
        "received_by",
        "created_at",
    ]
    list_filter = ["courier_name", "created_at"]
    search_fields = ["courier_name", "handed_by", "received_by", "remark"]
    readonly_fields = ["inbound_count", "pickup_exception_count", "return_processed_count", "created_at"]


@admin.register(PickupException)
class PickupExceptionAdmin(admin.ModelAdmin):
    list_display = [
        "exception_type",
        "operator",
        "parcel_tracking_no",
        "pickup_code",
        "created_at",
    ]
    list_filter = ["exception_type", "operator", "created_at"]
    search_fields = ["parcel_tracking_no", "pickup_code", "operator", "description"]
    readonly_fields = ["created_at"]
