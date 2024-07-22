from django.db import models
import datetime


# Create your models here.
class tbldistrict(models.Model):
    districtid = models.AutoField(primary_key=True)
    districtname = models.CharField(max_length=50)


class tbllocation(models.Model):
    locationid = models.AutoField(primary_key=True)
    locationname = models.CharField(max_length=50)
    districtid = models.ForeignKey(tbldistrict, on_delete=models.CASCADE, default="")


class tblcategory(models.Model):
    categoryid = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=50)
    categoryphoto = models.ImageField()


class tblmaterial(models.Model):
    materialid = models.AutoField(primary_key=True)
    materialtype = models.CharField(max_length=50)


class tblsubmaterial(models.Model):
    submaterialid = models.AutoField(primary_key=True)
    submaterialtype = models.CharField(max_length=50)
    materialid = models.ForeignKey(tblmaterial, on_delete=models.CASCADE, default="")


class tblpattern(models.Model):
    patternid = models.AutoField(primary_key=True)
    patternname = models.CharField(max_length=50)
    patternphoto = models.ImageField()
    submaterialid = models.ForeignKey(tblsubmaterial, on_delete=models.CASCADE, default="")


class tblcolor(models.Model):
    colorid = models.AutoField(primary_key=True)
    colorname = models.CharField(max_length=50)


class tblproduct(models.Model):
    productid = models.AutoField(primary_key=True)
    productname = models.CharField(max_length=50)
    productphoto = models.ImageField()
    price = models.IntegerField(max_length=50)
    description = models.CharField(max_length=500)
    categoryid = models.ForeignKey(tblcategory, on_delete=models.CASCADE, default="")
    patternid = models.ForeignKey(tblpattern, on_delete=models.CASCADE, default="")

class tblsize(models.Model):
    sizeid = models.AutoField(primary_key=True)
    sizename = models.CharField(max_length=50)
    productid = models.ForeignKey(tblproduct, on_delete=models.CASCADE, default="")
    materialquantity = models.IntegerField(max_length=50)


class tblpurchase(models.Model):
    purchaseid = models.AutoField(primary_key=True)
    billnumber = models.IntegerField(max_length=50)
    purchaseamount = models.IntegerField(max_length=50)
    discount = models.IntegerField(max_length=50)
    purchasetotal = models.IntegerField(max_length=50)
    purchasedate = models.DateField(default=datetime.date.today())


class tblpurchasedetails(models.Model):
    purchasedetailsid = models.AutoField(primary_key=True)
    purchasequantity = models.IntegerField(max_length=50)
    colorid = models.ForeignKey(tblcolor, on_delete=models.CASCADE, default="")
    patternid = models.ForeignKey(tblpattern, on_delete=models.CASCADE, default="")
    purchaseid = models.ForeignKey(tblpurchase, on_delete=models.CASCADE, default="")


class tblstock(models.Model):
    stockid = models.AutoField(primary_key=True)
    colorid = models.ForeignKey(tblcolor, on_delete=models.CASCADE, default="")
    patternid = models.ForeignKey(tblpattern, on_delete=models.CASCADE, default="")
    stockquantity = models.IntegerField(max_length=50)
