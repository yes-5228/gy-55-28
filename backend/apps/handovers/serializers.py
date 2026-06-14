from rest_framework import serializers

from .models import PickupException, ShiftHandover


class PickupExceptionSerializer(serializers.ModelSerializer):
    exception_type_label = serializers.CharField(source="get_exception_type_display", read_only=True)

    class Meta:
        model = PickupException
        fields = [
            "id",
            "parcel_tracking_no",
            "pickup_code",
            "exception_type",
            "exception_type_label",
            "operator",
            "description",
            "created_at",
        ]
        read_only_fields = ["created_at"]


class ShiftHandoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftHandover
        fields = [
            "id",
            "courier_name",
            "shift_start",
            "shift_end",
            "inbound_count",
            "pickup_exception_count",
            "return_processed_count",
            "remark",
            "handed_by",
            "received_by",
            "created_at",
        ]
        read_only_fields = ["inbound_count", "pickup_exception_count", "return_processed_count", "created_at"]


class ShiftHandoverCreateSerializer(serializers.Serializer):
    courier_name = serializers.CharField(max_length=40)
    shift_start = serializers.DateTimeField()
    shift_end = serializers.DateTimeField()
    remark = serializers.CharField(max_length=200, required=False, allow_blank=True)
    handed_by = serializers.CharField(max_length=40)
    received_by = serializers.CharField(max_length=40, required=False, allow_blank=True)


class ShiftStatsSerializer(serializers.Serializer):
    inbound_count = serializers.IntegerField()
    pickup_exception_count = serializers.IntegerField()
    return_processed_count = serializers.IntegerField()
