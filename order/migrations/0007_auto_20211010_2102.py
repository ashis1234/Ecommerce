# Generated by Django 3.0.7 on 2021-10-10 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210923_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
