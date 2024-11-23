# Generated by Django 4.2.3 on 2024-11-20 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0001_initial'),
        ('recipe', '0006_recipe_preffered_cuisine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='preffered_cuisine',
        ),
        migrations.AddField(
            model_name='recipe',
            name='cuisine',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cuisine', to='preferences.cuisine'),
            preserve_default=False,
        ),
    ]