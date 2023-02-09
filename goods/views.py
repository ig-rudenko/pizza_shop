from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import PizzasAddForm, CreateOrderForm
from .models import Pizza, Orders
from .cart import PizzaCart


class PizzaListView(View):
    def get(self, request):
        return render(
            request,
            "list_all.html",
            {"pizzas": Pizza.objects.all(), "cart": PizzaCart(request)},
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

            for pizza_order in cart.create_objects().pizzas:
                Orders.objects.create(
                    pizza=pizza_order,
                    count=pizza_order.count,
                    diameter=pizza_order.diameter,
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                    name=form.cleaned_data["name"],
                    payment=form.cleaned_data["payment"],
                )

            cart.clear()
            return render(request, "thanks.html")

        return render(request, "cart.html", {"cart": cart, "form": form})
