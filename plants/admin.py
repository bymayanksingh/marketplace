from django.contrib import admin

from plants.models import (Cart, CartItem, Category, Order, OrderItem, Plant,
                           User)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Plant)
admin.site.register(User)
