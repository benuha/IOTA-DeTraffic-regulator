from django.db import models


# Create your models here.
class TrafficNode(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=100)
    status = models.CharField(max_length=200)
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    # longitude = models.DecimalField(
    #             max_digits=9, decimal_places=6, null=True, blank=True)
    # latitude = models.DecimalField(
    #             max_digits=9, decimal_places=6, null=True, blank=True)
