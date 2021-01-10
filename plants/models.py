from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Plant(models.Model):

    # you need to associate creation of plants with a nursery
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    category = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(default="description")
    img_url = models.TextField(default="")

    class Meta:
        db_table = "plants"
        ordering = ["-name"]

    def __str__(self):
        return self.name



class Orders(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    products = ArrayField(models.CharField(max_length=50), default=list)
    quantities = ArrayField(models.PositiveIntegerField(), default=list)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    payment_method = models.CharField(max_length=30, default="COD")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "orders"
