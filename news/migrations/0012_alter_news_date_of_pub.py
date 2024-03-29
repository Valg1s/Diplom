# Generated by Django 4.1 on 2023-03-29 07:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0011_alter_news_date_of_pub"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="date_of_pub",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 29, 7, 21, 26, 230111, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата публікації",
            ),
        ),
    ]
