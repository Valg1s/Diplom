# Generated by Django 4.1 on 2023-04-06 18:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0014_alter_news_date_of_pub"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="date_of_pub",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 4, 6, 18, 12, 43, 586127, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата публікації",
            ),
        ),
    ]
