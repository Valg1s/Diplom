# Generated by Django 4.1 on 2023-01-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_playerstatistic_defence_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(default='standartpassword', max_length=200, verbose_name='Пароль'),
        ),
    ]
