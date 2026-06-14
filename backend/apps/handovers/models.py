from django.db import models


class PickupException(models.Model):
    class Type(models.TextChoices):
        WRONG_CODE = "wrong_code", "取件码错误"
        NOT_FOUND = "not_found", "快件不存在"
        DAMAGED = "damaged", "快件破损"
        OTHER = "other", "其他异常"

    parcel_tracking_no = models.CharField(max_length=50, blank=True)
    pickup_code = models.CharField(max_length=12, blank=True)
    exception_type = models.CharField(max_length=20, choices=Type.choices, default=Type.OTHER)
    operator = models.CharField(max_length=40)
    description = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "取件异常"
        verbose_name_plural = "取件异常"

    def __str__(self):
        return f"{self.get_exception_type_display()} - {self.operator}"


class ShiftHandover(models.Model):
    courier_name = models.CharField(max_length=40)
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    inbound_count = models.IntegerField(default=0)
    pickup_exception_count = models.IntegerField(default=0)
    return_processed_count = models.IntegerField(default=0)
    remark = models.CharField(max_length=200, blank=True)
    handed_by = models.CharField(max_length=40)
    received_by = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "交接班记录"
        verbose_name_plural = "交接班记录"

    def __str__(self):
        return f"{self.courier_name} - {self.shift_start.strftime('%Y-%m-%d')}"
