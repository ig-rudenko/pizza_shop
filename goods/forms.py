from django import forms
from django.core.exceptions import ValidationError
from .models import Orders


class PizzasAddForm(forms.Form):
    count = forms.IntegerField(min_value=1, max_value=10, required=True)
    diameter = forms.IntegerField(required=True)

    def clean_diameter(self):
        if self.cleaned_data["diameter"] not in [20, 25, 30, 50]:
            raise ValidationError("Неверный диаметр пиццы")
        return self.cleaned_data["diameter"]


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Orders
        fields = ["name", "phone", "address", "payment"]
