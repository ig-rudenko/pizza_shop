from django import test
from django.contrib.auth import get_user_model
from django.core.files import File
from django.conf import settings
from ..models import Pizza, Orders

User = get_user_model()


class TestCart(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User(username="user", email="user@mail", is_superuser=True)
        user.set_password("password")
        user.save()
        Pizza.objects.create(
            name="pizza1",
            about="nice pizza",
            cost=1000,
            image=File(open(f"{settings.BASE_DIR}/manage.py", "rb"), "image_test.jpg")
        )

    def test_buy_pizza(self):
        # Добавления пиццы в корзину
        self.client.post("/add/1", {"count": 2, "diameter": 25})

        print(self.client.session["cart"])

        resp = self.client.post(
            "/cart",
            {
                "name": "user",
                "phone": "123123123",
                "address": "fajskdjfkl",
                "payment": "card"
            }
        )

        print(resp.status_code)

        print(self.client.session["orders"])

        print(Orders.objects.get(id=1))
