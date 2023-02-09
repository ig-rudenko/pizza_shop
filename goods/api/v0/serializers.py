from rest_framework import serializers
from ...models import Pizza, Orders


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = "__all__"

    def to_representation(self, instance: Pizza):
        res = super().to_representation(instance)
        res["cost"] = instance.diameters_cost
        return res


class OrderSerializer(serializers.ModelSerializer):
    pizza_detail = PizzaSerializer(source="pizza", read_only=True)

    class Meta:
        model = Orders
        fields = "__all__"
        read_only_fields = ["cost"]
