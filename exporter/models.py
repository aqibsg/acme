from django.db import models

# Create your models here.
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500)
    active = models.BooleanField()

    def __str__(self):
        return self.sku  