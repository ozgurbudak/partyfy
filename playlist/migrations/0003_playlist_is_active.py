# Generated by Django 2.2.2 on 2019-07-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0002_playlist_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
