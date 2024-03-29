# Generated by Django 4.1 on 2023-03-26 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("team", "0002_alter_team_players"),
        ("games", "0003_statement_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="statement",
            name="coach",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="coach_statements",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Тренер",
            ),
        ),
        migrations.AlterField(
            model_name="statement",
            name="context",
            field=models.CharField(max_length=1024, verbose_name="Повідомлення"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="date",
            field=models.DateField(verbose_name="Дата"),
        ),
        migrations.AlterField(
            model_name="statement",
            name="status",
            field=models.IntegerField(
                choices=[(0, "Не розглянута"), (1, "Схвалено"), (2, "Відхилено")],
                default=0,
                verbose_name="Статус заяви",
            ),
        ),
        migrations.AlterField(
            model_name="statement",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="team_statements",
                to="team.team",
                verbose_name="Команда",
            ),
        ),
        migrations.AlterField(
            model_name="statement",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="tournament_statements",
                to="games.tournament",
                verbose_name="Турнір",
            ),
        ),
    ]
