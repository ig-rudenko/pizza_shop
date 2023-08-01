from django import test
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework import status
from ..models import Pizza

User = get_user_model()


class TestAPICreatePizza(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        Pizza.objects.create(
            name="pizza1",
            about="nice pizza",
            cost=1000,
            image=File(open(f"{settings.BASE_DIR}/static/img/pizza.png", "rb"), "image_test.jpg"),
        )

        superuser_data = {"username": "super", "password": "password"}
        user_data = {"username": "user123", "password": "password"}

        User.objects.create_user(is_superuser=True, **superuser_data)
        User.objects.create_user(**user_data)

        cls.superuser_data = superuser_data
        cls.user_data = user_data

        cls.pizza_data = {
            "name": "pizza2",
            "about": "nice pizza",
            "cost": 999,
            "image": SimpleUploadedFile(
                "image_test.jpg", open(f"{settings.BASE_DIR}/static/img/pizza.png", "rb").read()
            ),
        }

    def setUp(self) -> None:
        self.superuser_tokens = self.client.post("/api/token/", self.superuser_data).json()
        self.user_tokens = self.client.post("/api/token/", self.user_data).json()

    def test_get_pizza_list(self):
        resp = self.client.get("/api/v1/pizzas")

        pizza = Pizza.objects.get(name="pizza1")

        data = resp.json()
        print(data)
        self.assertTrue(data)
        self.assertEqual(data[0]["cost"], pizza.diameters_cost)

    def test_create_pizza_form_superuser(self):
        resp = self.client.post(
            "/api/v1/pizzas",
            self.pizza_data,
            HTTP_AUTHORIZATION=f"Bearer {self.superuser_tokens.get('access')}",
        )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(type(resp.json()["cost"]), list)

    def test_create_pizza_form_common_user(self):
        resp = self.client.post(
            "/api/v1/pizzas",
            self.pizza_data,
            HTTP_AUTHORIZATION=f"Bearer {self.user_tokens.get('access')}",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_pizza_without_token(self):
        resp = self.client.post("/api/v1/pizzas", self.pizza_data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
