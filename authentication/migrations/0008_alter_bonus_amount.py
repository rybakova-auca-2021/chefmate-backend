# Generated by Django 4.2.3 on 2023-10-12 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_branch_coupon_bonus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bonus',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
