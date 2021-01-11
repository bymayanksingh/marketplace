from django.contrib.auth.models import User
from rest_framework import serializers

from plants.models import Orders, Plant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}


class PlantSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Plant
        fields = (
            "id",
            "name",
            "description",
            "price",
            "category",
            "quantity",
            "img_url",
            "owner",
        )


class OrdersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Orders
        fields = (
            "date",
            "plants",
            "quantities",
            "total_price",
            "payment_method",
            "owner",
        )
