# Generated by Django 4.1 on 2023-04-06 09:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0008_alter_customuser_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="date_of_birth",
            field=models.DateField(
                blank=True, null=True, verbose_name="Дата народження"
            ),
        ),
    ]