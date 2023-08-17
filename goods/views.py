from concurrent.futures import ThreadPoolExecutor

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import PizzasAddForm, CreateOrderForm
from .models import Pizza, Orders
from .cart import PizzaCart


class PizzaListView(View):
    def get(self, request):

        pizzas_list = []

        with ThreadPoolExecutor() as executor:
            for pizza in Pizza.objects.all():
                executor.submit(self._add_pizza_data, pizza, pizzas_list)

        return render(
            request,
            "list_all.html",
            {"pizzas": pizzas_list, "cart": PizzaCart(request)},
        )

    @staticmethod
    def _add_pizza_data(pizza: Pizza, pizzas_list: list):
        pizzas_list.append(
            {
                "id": pizza.id,
                "name": pizza.name,
                "image_url": pizza.image.url,
                "hot": pizza.hot,
                "vegan": pizza.vegan,
                "cost": pizza.cost,
            }
        )


class PizzaView(View):
    def get(self, request, pizza_id: int):

        print(request.COOKIES)
        print(dict(request.session))

        return render(
            request,
            "show_pizza.html",
            {
                "pizza": get_object_or_404(Pizza, id=pizza_id),
                "cart": PizzaCart(request),
            },
        )


class AddPizzaView(View):
    def post(self, request, pizza_id: int):
        pizza = get_object_or_404(Pizza, id=pizza_id)
        form = PizzasAddForm(request.POST)
        if form.is_valid():
            cart = PizzaCart(request)
            cart.add(
                product=pizza,
                diameter=form.cleaned_data["diameter"],
                quantity=form.cleaned_data["count"],
                update_quantity=True,
            )
        return redirect("pizzas-list")


class ShowCartView(View):
    def get(self, request):
        cart = PizzaCart(request).create_objects()
        if cart:
            return render(
                request, "cart.html", {"cart": cart, "form": CreateOrderForm()}
            )
        return redirect("pizzas-list")

    def post(self, request):
        form = CreateOrderForm(request.POST)
        cart = PizzaCart(request).create_objects()

        if form.is_valid():
            orders = []
            for pizza_order in cart.create_objects().pizzas:
                order = Orders.objects.create(
                    pizza=pizza_order,
                    count=pizza_order.count,
                    diameter=pizza_order.diameter,
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    name=form.cleaned_data["name"],
                    payment=form.cleaned_data["payment"],
                )
                orders.append(order.id)

            cart.clear()

            new_cart = PizzaCart(request)
            new_cart.orders = orders
            new_cart.save()
            print(dict(request.session))

            return render(request, "thanks.html")

        return render(request, "cart.html", {"cart": cart, "form": form})
