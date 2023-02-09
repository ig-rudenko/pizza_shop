"""pizza_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from goods import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v0/", include("goods.api.v0.urls")),
    path("api/v1/", include("goods.api.v1.urls")),

    path("", views.PizzaListView.as_view(), name="pizzas-list"),
    path("pizza/<int:pizza_id>", views.PizzaView.as_view(), name="show-pizza"),
    path("add/<int:pizza_id>", views.AddPizzaView.as_view(), name="add-pizza"),
    path("cart", views.ShowCartView.as_view(), name="show-cart"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
