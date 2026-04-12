from django.db import models

class SmartBin(models.Model):
    location = models.CharField(max_length=100)
    fullness_percentage = models.IntegerField(default=0)
    last_collected = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    bin_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    capacity = models.CharField(max_length=50, blank=True)
    bin_type = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, default='Normal')
    collection_schedule = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.location} Bin - {self.fullness_percentage}% Full"


class MaintenanceAlert(models.Model):
    ALERT_TYPES = [
        ('full', 'Bin Full'),
        ('jammed', 'Bin Jammed'),
        ('damaged', 'Bin Damaged'),
    ]

    bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    message = models.TextField(blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.alert_type} - {self.bin.location}"