# Generated by Django 4.1 on 2023-01-03 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('news_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('content', models.CharField(max_length=1024)),
                ('photo_content', models.ImageField(default='default.png', upload_to='')),
                ('date_of_pub', models.DateTimeField()),
            ],
        ),
    ]
