# Generated by Django 4.1 on 2023-01-03 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
