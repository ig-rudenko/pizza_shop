from django import test
from django.contrib.auth import get_user_model
from django.core.files import File
from django.conf import settings
from django.shortcuts import reverse

from ..models import Pizza, Orders

User = get_user_model()


class TestCart(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pizza = Pizza.objects.create(
            name="pizza1",
            about="nice pizza",
            cost=1000,
            image=File(open(f"{settings.BASE_DIR}/static/img/pizza.png", "rb"), "image_test.jpg"),
        )
        cls.order_data = {
            "name": "user",
            "phone": "123123123",
            "address": "fajskdjfkl",
            "payment": "card",
        }
        cls.invalid_order_data = {
            "name": "",
            "phone": "+123123123",
            "address": "",
            "payment": "asdasdasd",
        }

    def test_buy_pizza(self):
        pizzas_count = 2
        pizzas_diameter = 25

        # Добавления пиццы в корзину
        self.client.post(
            reverse("add-pizza", args=(self.pizza.id,)),
            {"count": pizzas_count, "diameter": pizzas_diameter},
        )

        # Проверяем, что в корзине есть ключ, как строка идентификатора пиццы.
        cart_key = str(self.pizza.id)
        self.assertIn(cart_key, self.client.session["cart"])

        # В корзине только один заказ
        self.assertEqual(
            len(self.client.session["cart"]),
            1,
        )

        # Верный диаметр в корзине
        self.assertEqual(
            self.client.session["cart"][cart_key]["diameter"],
            pizzas_diameter,
        )

        # Верное кол-во в корзине
        self.assertEqual(
            self.client.session["cart"][cart_key]["quantity"],
            pizzas_count,
        )

        # Оформляем заказ
        resp = self.client.post(reverse("show-cart"), self.order_data)
        self.assertEqual(resp.status_code, 200)

        # После покупки, в корзине нет товаров
        # Но имеется запись о заказе
        order = Orders.objects.get(**self.order_data)

        # Наш заказ есть в списке заказов
        self.assertListEqual(
            self.client.session["orders"],
            [order.id],
        )

        # Корзина теперь пустая
        self.assertFalse(self.client.session["cart"])

    def test_invalid_buy_pizza(self):
        pizzas_count = 2
        pizzas_diameter = 25

        # Добавления пиццы в корзину
        self.client.post(
            reverse("add-pizza", args=(self.pizza.id,)),
            {"count": pizzas_count, "diameter": pizzas_diameter},
        )

        resp = self.client.post(reverse("show-cart"), self.invalid_order_data)

        self.assertTrue(resp.context["form"].errors)

        self.assertEqual(
            Orders.objects.count(),
            0,
        )

    def test_invalid_diameter_buy_pizza(self):
        pizzas_count = 2
        pizzas_diameter = 123123123

        # Добавления пиццы в корзину
        self.client.post(
            reverse("add-pizza", args=(self.pizza.id,)),
            {"count": pizzas_count, "diameter": pizzas_diameter},
        )

        self.assertNotIn("cart", self.client.session)

    def test_invalid_count_buy_pizza(self):
        pizzas_count = 20
        pizzas_diameter = 25

        # Добавления пиццы в корзину
        self.client.post(
            reverse("add-pizza", args=(self.pizza.id,)),
            {"count": pizzas_count, "diameter": pizzas_diameter},
        )

        self.assertNotIn("cart", self.client.session)

        pizzas_count = 0
        # Добавления пиццы в корзину
        self.client.post(
            reverse("add-pizza", args=(self.pizza.id,)),
            {"count": pizzas_count, "diameter": pizzas_diameter},
        )

        self.assertNotIn("cart", self.client.session)
