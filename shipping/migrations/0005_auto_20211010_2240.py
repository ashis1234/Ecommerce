# Generated by Django 3.0.7 on 2021-10-10 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0004_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='transcaction_hash',
            new_name='paymentID',
        ),
        migrations.AddField(
            model_name='transaction',
            name='paymentToken',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
