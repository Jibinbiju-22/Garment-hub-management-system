# Generated by Django 5.0.2 on 2024-03-03 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0021_alter_tblpurchase_purchasedate'),
        ('customerapp', '0004_rename_size_tblbookingdetails_sizeid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblbookingdetails',
            name='sizeid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='adminapp.tblsize'),
        ),
    ]
