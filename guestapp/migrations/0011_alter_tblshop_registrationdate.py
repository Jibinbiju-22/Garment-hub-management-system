# Generated by Django 5.0.2 on 2024-03-05 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guestapp', '0010_alter_tblshop_registrationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblshop',
            name='registrationdate',
            field=models.DateField(default=datetime.date(2024, 3, 6)),
        ),
    ]
