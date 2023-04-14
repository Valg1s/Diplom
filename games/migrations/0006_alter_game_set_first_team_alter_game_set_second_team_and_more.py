# Generated by Django 4.1 on 2023-04-06 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("games", "0005_game_set_first_team_game_set_second_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="set_first_team",
            field=models.IntegerField(
                default=0, verbose_name="Виграні сети першої команди"
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="set_second_team",
            field=models.IntegerField(
                default=0, verbose_name="Виграні сети другої команди"
            ),
        ),
        migrations.AlterField(
            model_name="game",
            name="tournament",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="tournament_game",
                to="games.tournament",
                verbose_name="Турнір(Назва турніру чи товариська гра)",
            ),
        ),
    ]