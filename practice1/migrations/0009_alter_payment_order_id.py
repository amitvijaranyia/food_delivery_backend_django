# Generated by Django 3.2.6 on 2021-08-25 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice1', '0008_alter_payment_payment_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='order_id',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]