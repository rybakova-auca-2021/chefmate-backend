# Generated by Django 4.2.3 on 2024-10-27 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_remove_bonus_hello_user_confirm_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_photos/'),
        ),
    ]
