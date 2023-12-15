# Define the QuickBiteDocument model representing the QuickBite table in the database
from django.db import models

class QuickBiteDocument(models.Model):
    # Fields for the QuickBiteDocument model
    Id = models.IntegerField()
    Name = models.CharField(max_length=255)
    Rating = models.FloatField()
    Discount = models.FloatField(null=True, blank=True)
    CashBack = models.FloatField()
    Cost_for_Two = models.FloatField(null=True, blank=True)
    City = models.CharField(max_length=255)
    Locality = models.CharField(max_length=255)
    Home_Delivery = models.BooleanField()
    Manu_Count = models.IntegerField()

    class Meta:
        # Define the database table name for the QuickBiteDocument model
        db_table = 'QuickBite'
