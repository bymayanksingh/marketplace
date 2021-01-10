from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from plants.views import OrdersViewSet, PlantViewSet, UserViewSet

router = DefaultRouter()
router.register(r"plants", PlantViewSet)
router.register(r"orders", OrdersViewSet)
router.register(r"users", UserViewSet)

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Nursery Marketplace API",
        default_version="v1",
        description="Nursery Marketplace API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^api/", include(router.urls)),
    url(r"^api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    url(r"^api-token-auth/", obtain_jwt_token),
    url(r"^api-token-verify/", verify_jwt_token),
    url(r"^api-token-refresh/", refresh_jwt_token),
    url(
        r"^docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
