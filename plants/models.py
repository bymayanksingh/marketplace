from django.contrib.auth.models import AbstractUser
from django.db import models

from marketplace import settings


class User(AbstractUser):
    handle = models.CharField(max_length=128, default="", blank=True)


class PlantQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class PlantManager(models.Manager):
    def get_queryset(self):
        return PlantQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        return self.get_queryset().active()


class Plant(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    category = models.ManyToManyField("Category", blank=True)
    inventory = models.PositiveIntegerField(default=0)

    objects = PlantManager()

    class Meta:
        ordering = ["-name"]

    def __str__(self):  # def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="cart", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    """A model that contains data for an item in the shopping cart."""

    cart = models.ForeignKey(
        Cart, related_name="items", on_delete=models.CASCADE, null=True, blank=True
    )
    plant = models.ForeignKey(Plant, related_name="items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.plant.name, self.quantity)


class Order(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="orders",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    plant = models.ForeignKey(
        Plant, related_name="order_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.plant.name, self.quantity)
