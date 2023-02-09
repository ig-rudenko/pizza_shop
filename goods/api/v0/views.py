from rest_framework import viewsets, pagination

from .serializers import PizzaSerializer, OrderSerializer
from ...models import Pizza, Orders


class PizzaPaginator(pagination.PageNumberPagination):
    page_size = 4


class PizzaControlViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer
    lookup_url_kwarg = "pizza_id"
    pagination_class = PizzaPaginator

    def get_queryset(self):
        queryset = Pizza.objects.all()

        if self.request.query_params.get("hot"):
            queryset = queryset.filter(hot=True)
        if self.request.query_params.get("vegan"):
            queryset = queryset.filter(vegan=True)
        return queryset


class OrderControlViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    lookup_url_kwarg = "order_id"
