# Generated by Django 5.0.3 on 2024-03-20 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0025_alter_tblpurchase_purchasedate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblpurchase',
            name='purchasedate',
            field=models.DateField(default=datetime.date(2024, 3, 20)),
        ),
    ]
