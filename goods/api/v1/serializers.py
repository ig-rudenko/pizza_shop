from rest_framework import serializers
from ...models import Pizza, Orders


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = "__all__"

    def to_representation(self, instance: Pizza) -> dict:
        """Сериализует данные"""
        result: dict = super().to_representation(instance)
        # Добавляем к ним свои
        result["cost"] = instance.diameters_cost

        return result


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = "__all__"
        read_only_fields = ["datetime", "cost"]
