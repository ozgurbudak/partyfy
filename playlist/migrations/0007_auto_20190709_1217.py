# Generated by Django 2.2.2 on 2019-07-09 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlist', '0006_suser_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='requests',
            field=models.ManyToManyField(blank=True, related_name='requests', to='playlist.Suser'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, related_name='allowed_users', to='playlist.Suser'),
        ),
    ]
