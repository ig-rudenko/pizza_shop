from django import test
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from ..models import Pizza

User = get_user_model()


class TestAPICreatePizza(test.TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User(username="user", email="user@mail", is_superuser=True)
        user.set_password("password")
        user.save()
        pizza = Pizza.objects.create(
            name="pizza1",
            about="nice pizza",
            cost=1000,
            image=File(open(f"{settings.BASE_DIR}/manage.py", "rb"), "image_test.py")
        )

    def setUp(self) -> None:
        self.tokens = self.client.post(
            "/api/token/",
            {
                "username": "user",
                "password": "password"
            }
        ).json()

    def test_get_pizza_list(self):
        resp = self.client.get(
            "/api/v1/pizzas"
        )

        pizza = Pizza.objects.get(name="pizza1")

        data = resp.json()
        print(data)
        self.assertTrue(data)
        self.assertEqual(data[0]["cost"], pizza.diameters_cost)

    def test_create_pizza(self):
        resp = self.client.post(
            "/api/v1/pizzas",
            {
                "name": "pizza2",
                "about": "nice pizza",
                "cost": 999,
                "image": SimpleUploadedFile("image_test.py", open(f"{settings.BASE_DIR}/manage.py", "rb").read())
            },
            HTTP_AUTHORIZATION=f"Bearer {self.tokens.get('access')}"
        )

        print(resp.json())
        print(resp.status_code)
