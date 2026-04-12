from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    total_eco_points = models.IntegerField(default=0)

    def __str__(self):
        return self.display_name or self.user.username

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
        # Uses bin_id if available, otherwise location
        identifier = self.bin_id if self.bin_id else self.location
        return f"{identifier} - {self.fullness_percentage}% Full"


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


class DepositLog(models.Model):
    # Predefined list for the dropdown
    MATERIAL_CHOICES = [
        ('Polyethylene', 'Polyethylene'),
        ('Polypropylene', 'Polypropylene'),
        ('Plastic', 'Plastic'),
        ('Mixed Plastic', 'Mixed Plastic'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposit_logs')
    smart_bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE, related_name='logs')
    
    # Updated to use choices for the dropdown
    material = models.CharField(
        max_length=100, 
        choices=MATERIAL_CHOICES, 
        default='Polyethylene'
    )
    
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    reward_points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TXN-{self.id:03d} | {self.user.username} | {self.material}"