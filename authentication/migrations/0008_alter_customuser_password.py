# Generated by Django 4.1 on 2023-03-29 07:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0007_alter_customuser_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="password",
            field=models.CharField(blank=True, max_length=200, verbose_name="Пароль"),
        ),
    ]
