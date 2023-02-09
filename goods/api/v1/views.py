import datetime

from rest_framework.exceptions import ValidationError

from rest_framework import generics

from .serializers import OrdersSerializer, PizzaSerializer
from ...models import Pizza, Orders


class PizzasListAPIViewGEN(generics.ListCreateAPIView):
    """Смотрим и создаем пиццы"""

    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class PizzasControlAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    lookup_url_kwarg = "pizza_id"
    lookup_field = "id"


class OrdersListAPIViewGEN(generics.ListCreateAPIView):
    """Смотрим и создаем заказы"""

    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrdersControlAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    lookup_url_kwarg = "order_id"
    lookup_field = "id"

    def perform_update(self, serializer: OrdersSerializer):
        if serializer.instance.datetime.timestamp() <= (datetime.datetime.now() - datetime.timedelta(minutes=5)).timestamp():
            serializer.save()

        raise ValidationError("Уже нельзя изменить заказ")
