from django.db import models

class Gullar(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    address = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    soni = models.PositiveIntegerField()

    def __str__(self):
        return self.name
