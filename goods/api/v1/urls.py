from django.urls import path
from . import views

# /api/v1/

urlpatterns = [
    path("pizzas", views.PizzasListAPIViewGEN.as_view()),
    path("pizzas/<int:pizza_id>", views.PizzasControlAPIView.as_view()),
    path("orders", views.OrdersListAPIViewGEN.as_view()),
    path("orders/<int:order_id>", views.OrdersControlAPIView.as_view()),
]
