# Generated by Django 5.0.2 on 2024-03-03 19:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customerapp', '0003_alter_tblbooking_bookingdate_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tblbookingdetails',
            old_name='size',
            new_name='sizeid',
        ),
        migrations.AlterField(
            model_name='tblbooking',
            name='bookingdate',
            field=models.DateField(default=datetime.date(2024, 3, 4)),
        ),
        migrations.AlterField(
            model_name='tblpayment',
            name='paymentdate',
            field=models.DateField(default=datetime.date(2024, 3, 4)),
        ),
    ]
