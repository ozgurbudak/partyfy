# Generated by Django 2.2.2 on 2019-07-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0003_playlist_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='playlist_id',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
