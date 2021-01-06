from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from plants import views

schema_view = get_schema_view(
    openapi.Info(
        title="Nursery Marketplace API",
        default_version="v1",
        description="Nursery Marketplace API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"plants", views.PlantViewSet)
router.register(r"category", views.CategoryViewSet)
router.register(r"carts", views.CartViewSet)
router.register(r"cart_items", views.CartItemViewSet)
router.register(r"orders", views.OrderViewSet)
router.register(r"order_items", views.OrderItemViewSet)

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^", include(router.urls)),
    url(
        r"^docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
