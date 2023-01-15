# Generated by Django 4.1 on 2023-01-06 11:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_customuser_options_alter_customuser_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerStatistic',
            fields=[
                ('stat_id', models.AutoField(primary_key=True, serialize=False)),
                ('games', models.IntegerField(default=0, null=True)),
                ('points', models.IntegerField(default=0, null=True)),
                ('defence', models.IntegerField(default=0, null=True)),
                ('year', models.IntegerField(default=2023)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player_stat', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'статистику',
                'verbose_name_plural': 'Статистика',
            },
        ),
    ]