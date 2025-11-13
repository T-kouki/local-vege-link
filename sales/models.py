from django.db import models

class Sale(models.Model):
    farmer = models.CharField(max_length=100)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    @property
    def total_amount(self):
        return self.quantity * self.price_per_unit

    def __str__(self):
        return f"{self.farmer} - {self.product} ({self.date})"
