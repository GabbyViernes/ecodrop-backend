from django.db import models

class SmartBin(models.Model):
    location = models.CharField(max_length=100)
    fullness_percentage = models.IntegerField(default=0)
    last_collected = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.location} Bin - {self.fullness_percentage}% Full"