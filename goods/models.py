from django.db import models
from django.core.validators import (
    MinLengthValidator,
)
from django.contrib.auth import get_user_model
from django.urls import reverse

from ya_storage.storage import yandex_disk_storage

User = get_user_model()


class Pizza(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="pizza/", storage=yandex_disk_storage)
    cost = models.IntegerField()
    about = models.TextField()
    hot = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def diameters_cost(self) -> list[dict]:
        return [
            {"diameter": "20", "price": int(self.cost)},
            {"diameter": "25", "price": int(self.cost * 25 / 20)},
            {"diameter": "30", "price": int(self.cost * 30 / 20)},
            {"diameter": "50", "price": int(self.cost * 50 / 20)},
        ]

    def get_absolute_url(self):
        return reverse("show-pizza", args=[self.id])


class Orders(models.Model):
    PIZZA_DIAMETERS = (
        (20, "20 см"),
        (25, "25 см"),
        (30, "30 см"),
        (50, "50 см"),
    )
    PAYMENT_TYPE = (
        ("card", "Картой"),
        ("money", "Наличкой"),
    )

    pizza = models.ForeignKey(Pizza, related_name="orders", on_delete=models.CASCADE)
    phone = models.IntegerField()
    name = models.CharField(max_length=100, validators=[MinLengthValidator(4)])
    address = models.CharField(max_length=255)
    payment = models.CharField(choices=PAYMENT_TYPE, max_length=5)

    count = models.IntegerField()
    cost = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
    diameter = models.SmallIntegerField(choices=PIZZA_DIAMETERS)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.cost = self.count * self.pizza.cost * (self.diameter / 20)
        return super().save(force_insert, force_update, using, update_fields)
