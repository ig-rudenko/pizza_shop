from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path, include
from django.contrib.staticfiles.utils import settings
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
    TokenVerifyView,
)

# Это представление для пользовательского интерфейса Swagger.
schema_view = get_schema_view(
    # Это описание API.
    openapi.Info(
        title="Pizza API",
        default_version="v1",
        description=f"""
## Здесь вы можете посмотреть API для работы с PIZZA'S SHOP

Для работы с каждым endpoint `требуется токен` (JWT). Получить можно по URL `/api/token`.

Время жизни access токена - `{settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].seconds / 60} минут`
Время жизни refresh токена - `{settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]}`
        """
    ),
    # Это список всех конечных точек, которые будут отображаться в Swagger.
    patterns=[
        # path("api/v0/", include("goods.api.v0.urls")),
        path("api/v1/", include("goods.api.v1.urls")),
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ],
    authentication_classes=[
        SessionAuthentication,
        JWTAuthentication,
    ],
    # Это означает, что пользовательский интерфейс Swagger недоступен для общего доступа.
    public=True,
    # Это означает, что пользовательский интерфейс Swagger не является общедоступным.
    permission_classes=[permissions.IsAuthenticatedOrReadOnly],
)
