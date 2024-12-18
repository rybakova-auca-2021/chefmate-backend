# Generated by Django 4.2.3 on 2024-11-20 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0001_initial'),
        ('authentication', '0014_user_username_alter_user_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='preferred_cuisines',
            field=models.ManyToManyField(blank=True, related_name='users', to='preferences.cuisine'),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_food',
            field=models.ManyToManyField(blank=True, related_name='users', to='preferences.food'),
        ),
    ]
