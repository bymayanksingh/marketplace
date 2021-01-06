from django.db.models import F, FloatField, Sum
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from plants.models import (Cart, CartItem, Category, Order, OrderItem, Plant,
                           User)
from plants.serializers import (CartItemSerializer, CartSerializer,
                                CategorySerializer, OrderItemSerializer,
                                OrderSerializer, PlantSerializer,
                                UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=["post", "put"])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            plant = Plant.objects.get(pk=request.data["plant_id"])
            quantity = int(request.data["quantity"])
        except:
            return Response({"status": "fail"})

        if plant.available_inventory <= 0 or plant.available_inventory - quantity < 0:
            return Response({"status": "fail"})

        existing_cart_item = CartItem.objects.filter(cart=cart, plant=plant).first()
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = CartItem(cart=cart, plant=plant, quantity=quantity)
            new_cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True, methods=["post", "put"])
    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            plant = Plant.objects.get(pk=request.data["plant_id"])
        except:
            return Response({"status": "fail"})

        try:
            cart_item = CartItem.objects.get(cart=cart, plant=plant)
        except:
            return Response({"status": "fail"})

        if cart_item.quantity == 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        try:
            purchaser_id = self.request.data["customer"]
            user = User.objects.get(pk=purchaser_id)
        except:
            raise serializers.ValidationError("User was not found")

        cart = user.cart

        for cart_item in cart.items.all():
            if cart_item.plant.available_inventory - cart_item.quantity < 0:
                raise serializers.ValidationError(
                    "We do not have enough inventory of "
                    + str(cart_item.plant.name)
                    + "to complete your purchase. Sorry, we will restock soon"
                )

        total_aggregated_dict = cart.items.aggregate(
            total=Sum(F("quantity") * F("plant__price"), output_field=FloatField())
        )

        order_total = round(total_aggregated_dict["total"], 2)
        order = serializer.save(customer=user, total=order_total)

        order_items = []
        for cart_item in cart.items.all():
            order_items.append(
                OrderItem(
                    order=order, plant=cart_item.plant, quantity=cart_item.quantity
                )
            )
            cart_item.plant.available_inventory -= cart_item.quantity
            cart_item.plant.save()

        OrderItem.objects.bulk_create(order_items)

        cart.items.clear()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, url_path="order_history/(?P<customer_id>[0-9])")
    def order_history(self, request, customer_id):
        try:
            user = User.objects.get(id=customer_id)

        except:
            return Response({"status": "fail"})

        orders = Order.objects.filter(customer=user)
        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
