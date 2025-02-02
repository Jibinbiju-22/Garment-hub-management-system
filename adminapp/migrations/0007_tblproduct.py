# Generated by Django 4.1 on 2024-02-19 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_tblcolor'),
    ]

    operations = [
        migrations.CreateModel(
            name='tblproduct',
            fields=[
                ('productid', models.AutoField(primary_key=True, serialize=False)),
                ('productname', models.CharField(max_length=50)),
                ('productphoto', models.ImageField(upload_to='')),
                ('price', models.IntegerField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('patternid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='adminapp.tblpattern')),
            ],
        ),
    ]
