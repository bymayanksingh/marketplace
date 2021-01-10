from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from plants.models import Orders, Plant
from plants.permissions import IsOwnerOrReadOnly, IsStaffOrTargetUser
from plants.serializers import (
    OrdersSerializer,
    PlantSerializer,
    UserSerializer,
)


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all().order_by("-id")
    serializer_class = OrdersSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(owner=user.id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (
            (
                permissions.AllowAny()
                if self.request.method == "POST"
                else IsStaffOrTargetUser()
            ),
        )

    def perform_create(self, serializer):
        password = make_password(self.request.data["password"])
        serializer.save(password=password)

    def perform_update(self, serializer):
        password = make_password(self.request.data["password"])
        serializer.save(password=password)
