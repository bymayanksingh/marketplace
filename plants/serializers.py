from django.contrib.auth.models import User
from rest_framework import serializers

from plants.models import  Orders, Plant


class UserSerializer(serializers.ModelSerializer):
    plants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "products")
        extra_kwargs = {"password": {"write_only": True}}


class PlantSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Plant
        fields = "__all__"



class OrdersSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Orders
        fields = "__all__"
