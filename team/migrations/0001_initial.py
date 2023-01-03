# Generated by Django 4.1 on 2023-01-03 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=128, verbose_name='Назва команди')),
                ('year_of_create', models.IntegerField(default=2023, verbose_name='Рік створення')),
                ('logo', models.ImageField(default='default_logo.png', null=True, upload_to='', verbose_name='Логотип')),
                ('players', models.ManyToManyField(null=True, related_name='Гравець', to=settings.AUTH_USER_MODEL, verbose_name='Гравці')),
                ('team_coach', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Тренер', to=settings.AUTH_USER_MODEL, verbose_name='Тренер')),
            ],
            options={
                'verbose_name': 'команду',
                'verbose_name_plural': 'Команди',
            },
        ),
    ]