from django.db import models
from adminapp.models import *
from guestapp.models import *
# Create your models here.
class tblbooking(models.Model):
    bookingid = models.AutoField(primary_key=True)
    productid = models.ForeignKey(tblproduct, on_delete=models.CASCADE, default="")
    bookingdate = models.DateField(default=datetime.date.today())
    deliverydate = models.DateField()
    bookingstatus = models.CharField(max_length=50)
    loginid = models.ForeignKey(tbllogin, on_delete=models.CASCADE, default="")

class tblbookingdetails(models.Model):
    bookingdetailsid = models.AutoField(primary_key=True)
    colorid = models.ForeignKey(tblcolor, on_delete=models.CASCADE, default="")
    sizeid = models.ForeignKey(tblsize, on_delete=models.CASCADE, default="")
    bookingquantity = models.IntegerField(max_length=50)
    bookingamount = models.IntegerField(max_length=50)
    bookingid = models.ForeignKey(tblbooking, on_delete=models.CASCADE, default="")

class tblpayment(models.Model):
    paymentid = models.AutoField(primary_key=True)
    paymentamount = models.IntegerField(max_length=50)
    paymentdate = models.DateField(default=datetime.date.today())
    bookingid = models.ForeignKey(tblbooking, on_delete=models.CASCADE, default="")

class SearchHistory(models.Model):
    shopid = models.ForeignKey(tblshop, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
