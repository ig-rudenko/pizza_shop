from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Pizza, Orders


@register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    pass


@register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    pass
