# Generated by Django 4.1.6 on 2023-02-07 20:57

from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Pizza",
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
                ("name", models.CharField(max_length=255)),
                ("image", models.ImageField(upload_to="pizza/")),
                ("cost", models.IntegerField()),
                ("about", models.TextField()),
                ("hot", models.BooleanField(default=False)),
                ("vegan", models.BooleanField(default=False)),
            ],
        )
    ]
