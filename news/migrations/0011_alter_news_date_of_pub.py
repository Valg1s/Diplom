# Generated by Django 4.1 on 2023-03-26 08:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("news", "0010_alter_news_date_of_pub"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="date_of_pub",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 3, 26, 8, 23, 9, 740245, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Дата публікації",
            ),
        ),
    ]
