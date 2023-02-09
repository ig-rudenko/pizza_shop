# Generated by Django 4.1.6 on 2023-02-07 21:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("goods", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orders",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone", models.IntegerField()),
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        validators=[django.core.validators.MinLengthValidator(4)],
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                (
                    "payment",
                    models.CharField(
                        choices=[("card", "Картой"), ("money", "Наличкой")],
                        max_length=5,
                    ),
                ),
                ("count", models.IntegerField()),
                ("cost", models.IntegerField()),
                ("datetime", models.DateTimeField(auto_now_add=True)),
                (
                    "diameter",
                    models.SmallIntegerField(
                        choices=[
                            (20, "20 см"),
                            (25, "25 см"),
                            (30, "30 см"),
                            (50, "50 см"),
                        ]
                    ),
                ),
                (
                    "pizza",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to="goods.pizza",
                    ),
                ),
            ],
        ),
    ]
