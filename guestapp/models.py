from django.db import models
import datetime
from adminapp.models import *
# Create your models here.
class tbllogin(models.Model):
    loginid=models.AutoField(primary_key=True)
    email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    role=models.CharField(max_length=50)
    loginstatus = models.CharField(max_length=50)

class tblshop(models.Model):
    shopid=models.AutoField(primary_key=True)
    shopname=models.CharField(max_length=50)
    phone=models.BigIntegerField()
    address = models.CharField(max_length=500)
    shopphoto = models.ImageField()
    registrationdate = models.DateField(default=datetime.date.today())
    locationid=models.ForeignKey(tbllocation,on_delete=models.CASCADE,default="")
    loginid=models.ForeignKey(tbllogin, on_delete=models.CASCADE,default="")