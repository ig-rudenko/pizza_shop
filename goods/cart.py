from django.utils.safestring import mark_safe

from .models import Pizza


class PizzaCart:
    key = "cart"
    pizza_image = '<img height="40px" src="/static/img/pizza.png">'

    def __init__(self, request):
        """
        Инициализируем корзину
        """

        # request.session - хранилище данных пользователя
        # создаем свой объект
        self.session = request.session

        # Смотрим корзину пользователя self.session.get("cart")
        cart = self.session.get(self.key)
        if not cart:
            # Если её еще нет
            cart = self.session[self.key] = {}

        # Корзина
        self.cart = cart

        # Будущий список пицц
        self.pizzas = []

    def add(self, product: Pizza, diameter, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """

        # self.cart = {
        #     "2": {
        #         "diameter": 20,
        #         "quantity": 3
        #     },
        #     "5": {
        #         "diameter": 20,
        #         "quantity": 3
        #     }
        # }

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
            }
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.cart[product_id]["diameter"] = diameter
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[self.key] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def total_count(self):
        return len(self)

    def total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        if not self.pizzas:
            self.create_objects()
        price = 0
        for pizza in self.pizzas:
            price += pizza.total_cost
        return price

    def clear(self):
        # удаление корзины из сессии
        del self.session[self.key]
        self.session.modified = True

    def create_objects(self):
        self.pizzas = []
        pizzas = Pizza.objects.filter(id__in=list(map(int, self.cart.keys())))
        for pizza in pizzas:
            pizza: Pizza

            # СОЗДАЕМ СВОИ АТРИБУТЫ ДЛЯ ОБЪЕКТОВ ПИЦЦ
            pizza.count = self.cart[str(pizza.id)]["quantity"]
            pizza.diameter = self.cart[str(pizza.id)]["diameter"]
            # картинки
            pizza.count_images = mark_safe(self.pizza_image * pizza.count)
            # ====
            pizza.total_cost = pizza.count * pizza.cost * (pizza.diameter / 20)
            self.pizzas.append(pizza)
        return self
