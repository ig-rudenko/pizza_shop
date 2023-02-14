import datetime

from rest_framework.exceptions import ValidationError

from rest_framework import generics, permissions

from .serializers import OrdersSerializer, PizzaSerializer
from ...models import Pizza, Orders
from .permissions import IsSuperUserOrReadOnly, IsSuperUser, IsOrderOwner


class PizzasListAPIViewGEN(generics.ListCreateAPIView):
    """Смотрим и создаем пиццы"""

    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class PizzasControlAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    lookup_url_kwarg = "pizza_id"
    lookup_field = "id"
    permission_classes = [IsSuperUserOrReadOnly]


class OrdersListAPIViewGEN(generics.ListCreateAPIView):
    """Смотрим и создаем заказы"""

    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsSuperUser]


class OrdersControlAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    lookup_url_kwarg = "order_id"
    lookup_field = "id"
    permission_classes = [IsOrderOwner]

    def perform_update(self, serializer: OrdersSerializer):
        if serializer.instance.datetime.timestamp() <= (datetime.datetime.now() - datetime.timedelta(minutes=5)).timestamp():
            serializer.save()

        raise ValidationError("Уже нельзя изменить заказ")
