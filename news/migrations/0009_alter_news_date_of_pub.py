# Generated by Django 4.1 on 2023-01-12 11:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_news_date_of_pub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date_of_pub',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 12, 11, 10, 26, 72373, tzinfo=datetime.timezone.utc), verbose_name='Дата публікації'),
        ),
    ]
