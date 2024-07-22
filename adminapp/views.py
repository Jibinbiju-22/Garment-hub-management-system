from django.shortcuts import render
from adminapp.models import *
from guestapp.models import *
from customerapp.models import *
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Sum, Count
from django.contrib import messages
from django.views.decorators.cache import cache_control
from datetime import datetime
from django.core.serializers import serialize
import xlwt

from django.views.generic import View
from email.message import EmailMessage
import smtplib


# Create your views here.

# Home function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    stock = tblstock.objects.all()
    shop = tblshop.objects.all()
    return render(request, 'admin/home.html', {'shop': shop, 'stock': stock})


# District registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def districtregistration(request):
    if request.method == 'POST':
        districtname = request.POST.get('districtname')
        distictobj = tbldistrict()
        if tbldistrict.objects.filter(districtname=districtname).exists():
            return HttpResponse("<script>alert('Duplicate..');window.location='/admin/districtregistration';</script>")
        distictobj.districtname = districtname
        distictobj.save()
        return HttpResponse("<script>alert('Inserted..');window.location='/admin/districtregistration';</script>")
    else:
        return render(request, 'admin/districtregistration.html')


# Location registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def locationregistration(request):
    if request.method == 'POST':
        districtid = tbldistrict.objects.get(districtid=request.POST.get('districtid'))
        locationname = request.POST.get('locationname')
        locationobj = tbllocation()
        if tbllocation.objects.filter(districtid=districtid, locationname=locationname).exists():
            return HttpResponse(
                "<script>alert('Already exist');window.location='/admin/locationregistration';</script>")
        locationobj.districtid = districtid
        locationobj.locationname = locationname
        locationobj.save()
        return HttpResponse(
            "<script>alert('Location registered');window.location='/admin/locationregistration';</script>")
    else:
        district = tbldistrict.objects.all()
        return render(request, 'admin/locationregistration.html', {'district': district})


# Category registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def categoryregistration(request):
    if request.method == 'POST':
        categoryname = request.POST.get('categoryname')
        categoryphoto = request.FILES['categoryphoto']
        categoryobj = tblcategory()
        if tblcategory.objects.filter(categoryname=categoryname).exists():
            return HttpResponse(
                "<script>alert('Already exist');window.location='/admin/categoryregistration';</script>")
        categoryobj.categoryname = categoryname
        categoryobj.categoryphoto = categoryphoto
        categoryobj.save()
        return HttpResponse(
            "<script>alert('Category registered');window.location='/admin/categoryregistration';</script>")
    else:
        return render(request, 'admin/categoryregistration.html')

# Category exist function
def categoryexist(request):
    if request.method == 'POST':
        field_value = request.POST.get('categoryname')
        # Check if the data exists in the table
        exists = tblcategory.objects.filter(categoryname=field_value).values()
        return JsonResponse(list(exists), safe=False)



# Size registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sizeregistration(request):
    if request.method == 'POST':
        sizename = request.POST.get('sizename')
        materialquantity = request.POST.get('materialquantity')
        productid = tblproduct.objects.get(productid=request.POST.get('productid'))
        sizeobj = tblsize()
        if tblsize.objects.filter(productid=productid, sizename=sizename).exists():
            return HttpResponse(
                "<script>alert('Already exist');window.location='/admin/sizeregistration';</script>")
        sizeobj.sizename = sizename
        sizeobj.materialquantity = materialquantity
        sizeobj.productid = productid
        sizeobj.save()
        return HttpResponse(
            "<script>alert('Size registered');window.location='/admin/sizeregistration';</script>")
    else:
        category = tblcategory.objects.all()
        return render(request, 'admin/sizeregistration.html', {'category': category})


# Material registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def materialregistration(request):
    if request.method == 'POST':
        materialtype = request.POST.get('materialtype')
        materialobj = tblmaterial()
        if tblmaterial.objects.filter(materialtype=materialtype).exists():
            return HttpResponse("<script>alert('Duplicate..');window.location='/admin/materialregistration';</script>")
        materialobj.materialtype = materialtype
        materialobj.save()
        return HttpResponse("<script>alert('Inserted..');window.location='/admin/materialregistration';</script>")
    else:
        return render(request, 'admin/materialregistration.html')


# Sub material registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def submaterialregistration(request):
    if request.method == 'POST':
        materialid = tblmaterial.objects.get(materialid=request.POST.get('materialid'))
        submaterialtype = request.POST.get('submaterialtype')
        submaterialobj = tblsubmaterial()
        if tblsubmaterial.objects.filter(materialid=materialid, submaterialtype=submaterialtype).exists():
            return HttpResponse(
                "<script>alert('Already exist');window.location='/admin/submaterialregistration';</script>")
        submaterialobj.materialid = materialid
        submaterialobj.submaterialtype = submaterialtype
        submaterialobj.save()
        return HttpResponse(
            "<script>alert('Sub material registered');window.location='/admin/submaterialregistration';</script>")
    else:
        material = tblmaterial.objects.all()
        return render(request, 'admin/submaterialregistration.html', {'material': material})


# Pattern registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def patternregistration(request):
    if request.method == 'POST':
        submaterialid = tblsubmaterial.objects.get(submaterialid=request.POST.get('submaterialid'))
        patternname = request.POST.get('patternname')
        patternphoto = request.FILES['patternphoto']
        patternobj = tblpattern()
        if tblpattern.objects.filter(submaterialid=submaterialid, patternname=patternname).exists():
            return HttpResponse("<script>alert('Already exist');window.location='/admin/patternregistration';</script>")
        patternobj.submaterialid = submaterialid
        patternobj.patternname = patternname
        patternobj.patternphoto = patternphoto
        patternobj.save()
        return HttpResponse(
            "<script>alert('Pattern registered');window.location='/admin/patternregistration';</script>")
    else:
        material = tblmaterial.objects.all()
        return render(request, 'admin/patternregistration.html', {'material': material})


# Fill sub material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillsubmaterial(request):
    materialid = int(request.POST.get("materialid"))
    submaterial = tblsubmaterial.objects.filter(materialid=materialid).values()
    return JsonResponse(list(submaterial), safe=False)


# Color registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def colorregistration(request):
    if request.method == 'POST':
        colorname = request.POST.get('colorname')
        colorobj = tblcolor()
        if tblcolor.objects.filter(colorname=colorname).exists():
            return HttpResponse("<script>alert('Duplicate..');window.location='/admin/colorregistration';</script>")
        colorobj.colorname = colorname
        colorobj.save()
        return HttpResponse("<script>alert('Inserted..');window.location='/admin/colorregistration';</script>")
    else:
        return render(request, 'admin/colorregistration.html')


# Product registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def productregistration(request):
    if request.method == 'POST':
        patternid = tblpattern.objects.get(patternid=request.POST.get('patternid'))
        productname = request.POST.get('productname')
        productphoto = request.FILES['productphoto']
        price = request.POST.get('price')
        description = request.POST.get('description')
        categoryid = tblcategory.objects.get(categoryid=request.POST.get('categoryid'))
        productobj = tblproduct()
        if tblproduct.objects.filter(patternid=patternid, productname=productname).exists():
            return HttpResponse("<script>alert('Already exist');window.location='/admin/productregistration';</script>")
        productobj.patternid = patternid
        productobj.productname = productname
        productobj.productphoto = productphoto
        productobj.price = price
        productobj.description = description
        productobj.categoryid = categoryid
        productobj.save()
        return HttpResponse(
            "<script>alert('Product registered');window.location='/admin/productregistration';</script>")
    else:
        category = tblcategory.objects.all()
        material = tblmaterial.objects.all()
        return render(request, 'admin/productregistration.html', {'material': material, 'category': category})


# Fill pattern function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillpattern(request):
    submaterialid = int(request.POST.get("submaterialid"))
    pattern = tblpattern.objects.filter(submaterialid=submaterialid).values()
    return JsonResponse(list(pattern), safe=False)


# purchase function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def purchase(request):
    if request.method == 'POST':
        billnumber = request.POST.get('billnumber')
        purchaseamount = request.POST.get('purchaseamount')
        discount = request.POST.get('discount')
        purchasetotal = request.POST.get('purchasetotal')
        purchaseobj = tblpurchase()
        if tblpurchase.objects.filter(billnumber=billnumber).exists():
            return HttpResponse("<script>alert('Duplicate..');window.location='/admin/purchase';</script>")
        purchaseobj.billnumber = billnumber
        purchaseobj.purchaseamount = purchaseamount
        purchaseobj.discount = discount
        purchaseobj.purchasetotal = purchasetotal
        purchaseobj.save()
        return HttpResponse("<script>alert('Inserted..');window.location='/admin/purchasemore';</script>")
    else:
        return render(request, 'admin/purchase.html')


# purchase more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def purchasemore(request):
    if request.method == 'POST':
        purchaseid = tblpurchase.objects.get(purchaseid=request.POST.get('purchaseid'))
        colorid = tblcolor.objects.get(colorid=request.POST.get('colorid'))
        patternid = tblpattern.objects.get(patternid=request.POST.get('patternid'))
        purchasequantity = request.POST.get('purchasequantity')
        purchasedetailsobj = tblpurchasedetails()
        if tblpurchasedetails.objects.filter(purchaseid=purchaseid, colorid=colorid, patternid=patternid).exists():
            return HttpResponse("<script>alert('Already purchased..');window.location='/admin/purchasemore';</script>")
        purchasedetailsobj.purchaseid = purchaseid
        purchasedetailsobj.colorid = colorid
        purchasedetailsobj.patternid = patternid
        purchasedetailsobj.purchasequantity = purchasequantity
        purchasedetailsobj.save()
        stockobj = tblstock()
        if tblstock.objects.filter(colorid=colorid, patternid=patternid).exists():
            stock = tblstock.objects.get(colorid=colorid, patternid=patternid)
            squantity = int(stock.stockquantity)
            pquantity = int(purchasequantity)
            stock.stockquantity = squantity + pquantity
            stock.save()
            return HttpResponse("<script>alert('Inserted..');window.location='/admin/purchasemore';</script>")
        else:
            stockobj.colorid = colorid
            stockobj.patternid = patternid
            stockobj.stockquantity = purchasequantity
            stockobj.save()
            return HttpResponse("<script>alert('Inserted..');window.location='/admin/purchasemore';</script>")
    else:
        purchase = tblpurchase.objects.last()
        material = tblmaterial.objects.all()
        color = tblcolor.objects.all()
        return render(request, 'admin/purchasemore.html', {'material': material, 'color': color, 'purchase': purchase})


# View district function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewdistrict(request):
    district = tbldistrict.objects.all()
    return render(request, 'admin/viewdistrict.html', {'district': district})


# View material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewmaterial(request):
    material = tblmaterial.objects.all()
    return render(request, 'admin/viewmaterial.html', {'material': material})


# View color function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewcolor(request):
    color = tblcolor.objects.all()
    return render(request, 'admin/viewcolor.html', {'color': color})


# View category function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewcategory(request):
    category = tblcategory.objects.all()
    return render(request, 'admin/viewcategory.html', {'category': category})


# View size function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewsize(request):
    category = tblcategory.objects.all()
    return render(request, 'admin/viewsize.html', {'category': category})


# Function for size location
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillsize(request):
    productid = int(request.POST.get("productid"))
    size = tblsize.objects.filter(productid=productid).values()
    # Print the SQL query generated by Django
    return JsonResponse(list(size), safe=False)


# View location function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewlocation(request):
    district = tbldistrict.objects.all()
    row = tbldistrict.objects.first()
    location = tbllocation.objects.filter(districtid=row.districtid)
    return render(request, 'admin/viewlocation.html', {'district': district, 'location': location})


# Function for fill location
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filllocation(request):
    districtid = int(request.POST.get("districtid"))
    location = tbllocation.objects.filter(districtid=districtid).values()
    # Print the SQL query generated by Django
    return JsonResponse(list(location), safe=False)


# View sub material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewsubmaterial(request):
    material = tblmaterial.objects.all()
    row = tblmaterial.objects.first()
    submaterial = tblsubmaterial.objects.filter(materialid=row.materialid)
    return render(request, 'admin/viewsubmaterial.html', {'material': material, 'submaterial': submaterial})


# Function for fill sub material
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillsubmaterial(request):
    materialid = int(request.POST.get("materialid"))
    submaterial = tblsubmaterial.objects.filter(materialid=materialid).values()
    # Print the SQL query generated by Django
    return JsonResponse(list(submaterial), safe=False)


# View pattern function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpattern(request):
    material = tblmaterial.objects.all()
    return render(request, 'admin/viewpattern.html', {'material': material})


# Function for fill pattern for view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillpatternforview(request):
    submaterialid = int(request.POST.get("submaterialid"))
    pattern = tblpattern.objects.filter(submaterialid=submaterialid).values()
    # Print the SQL query generated by Django
    return JsonResponse(list(pattern), safe=False)


# View purchase function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpurchase(request):
    purchase = tblpurchase.objects.all()
    return render(request, 'admin/viewpurchase.html', {'purchase': purchase})


# View purchase details function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpurchasedetails(request, id):
    purchase = tblpurchase.objects.get(purchaseid=id)
    purchasedetails = tblpurchasedetails.objects.filter(purchaseid=id)
    return render(request, 'admin/viewpurchasedetails.html', {'purchasedetails': purchasedetails, 'purchase': purchase})


# View purchase details more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpurchasedetailsmore(request, id):
    pattern = tblpattern.objects.get(patternid=id)
    object = tblpattern.objects.filter(patternid=id)
    return render(request, 'admin/viewpurchasedetailsmore.html', {'pattern': pattern, 'object': object})


# View stock function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewstock(request):
    stock = tblstock.objects.all()
    return render(request, 'admin/viewstock.html', {'stock': stock})


# View stock more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewstockmore(request, id):
    pattern = tblpattern.objects.get(patternid=id)
    object = tblpattern.objects.filter(patternid=id)
    return render(request, 'admin/viewstockmore.html', {'pattern': pattern, 'object': object})


# View stock by material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewstockbymaterial(request):
    material = tblmaterial.objects.all()
    return render(request, 'admin/viewstockbymaterial.html', {'material': material})


# Function for fill stock
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillstock(request):
    patternid = int(request.POST.get("patternid"))
    stock = tblstock.objects.filter(patternid=patternid).values('stockid', 'patternid__patternname',
                                                                'patternid__patternphoto', 'colorid__colorname',
                                                                'stockquantity')
    # Print the SQL query generated by Django
    return JsonResponse(list(stock), safe=False)


# View product function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproduct(request):
    product = tblproduct.objects.all()
    return render(request, 'admin/viewproduct.html', {'product': product})


# View product more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproductmorebyadmin(request, id):
    product = tblproduct.objects.get(productid=id)
    object = tblproduct.objects.filter(productid=id)
    return render(request, 'admin/viewproductmorebyadmin.html', {'product': product, 'object': object})


# View product by category function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproductbycategory(request):
    category = tblcategory.objects.all()
    row = tblcategory.objects.first()
    product = tblproduct.objects.filter(categoryid=row.categoryid)
    return render(request, 'admin/viewproductbycategory.html', {'category': category, 'product': product})


# Function for fill product by category
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillproductbycategory(request):
    categoryid = int(request.POST.get("categoryid"))
    product = tblproduct.objects.filter(categoryid=categoryid).values()
    # Print the SQL query generated by Django
    return JsonResponse(list(product), safe=False)


# View product by pattern function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproductbypattern(request):
    material = tblmaterial.objects.all()
    return render(request, 'admin/viewproductbypattern.html', {'material': material})


# Function for fill product by pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillproductbypattern(request):
    patternid = int(request.POST.get("patternid"))
    product = tblproduct.objects.filter(patternid=patternid).values()
    # Print the SQL query generated by Django
    return JsonResponse(list(product), safe=False)


# View shop function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewshop(request):
    shop = tblshop.objects.all()
    return render(request, 'admin/viewshop.html', {'shop': shop})


# View shop more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewshopmore(request, id):
    shop = tblshop.objects.get(shopid=id)
    object = tblshop.objects.filter(shopid=id)
    return render(request, 'admin/viewshopmore.html', {'shop': shop, 'object': object})


# View shop by district function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewshopbydistrict(request):
    district = tbldistrict.objects.all()
    return render(request, 'admin/viewshopbydistrict.html', {'district': district})


# View shop by district function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillshop(request):
    locationid = int(request.POST.get("locationid"))
    shop = tblshop.objects.filter(locationid=locationid).values('shopid', 'shopname', 'shopphoto', 'phone',
                                                                'registrationdate', 'loginid__email')
    # Print the SQL query generated by Django
    return JsonResponse(list(shop), safe=False)


class ExportExcelShop(View):
    def get(self, request):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="shoplist.xls"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet1')

        # Define the column headings
        row_num = 0
        columns = ['Name', 'Email', 'Phone', 'Registration Date', 'Address', 'Location', 'Idkki']
        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        # Query the data from your model, and write it to the worksheet
        queryset = tblshop.objects.values_list('shopname', 'loginid__email', 'phone', 'registrationdate', 'address',
                                               'locationid__locationname', 'locationid__districtid__districtname')
        for row in queryset:
            row_num += 1
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response


# View booking function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewbooking(request):
    booking = tblbooking.objects.filter(
        Q(bookingstatus='Requested') | Q(bookingstatus='Confirmed'))
    return render(request, 'admin/viewbooking.html', {'booking': booking})


# View booking more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewbookingmore(request):
    if request.method == 'POST':
        bookingid = request.POST.get('bookingid')
        loginid = request.POST.get('loginid')
        shop = tblshop.objects.get(loginid=loginid)
        booking = tblbookingdetails.objects.filter(bookingid=bookingid)
        bookingamount = 0

        # Loop through each object and add the value of the specific column to the sum
        for obj in booking:
            # Assuming 'column_name' is the name of the column you want to sum
            bookingamount += obj.bookingamount
        product = tblbooking.objects.get(bookingid=bookingid)
        return render(request, 'admin/viewbookingmore.html',
                      {'booking': booking, 'shop': shop, 'product': product, 'bookingamount': bookingamount})


# View payment function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpayment(request):
    payment = tblpayment.objects.all()
    return render(request, 'admin/viewpayment.html', {'payment': payment})


# View payment more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpaymentmore(request):
    if request.method == 'POST':
        bookingid = request.POST.get('bookingid')
        loginid = request.POST.get('loginid')
        shop = tblshop.objects.get(loginid=loginid)
        booking = tblbookingdetails.objects.filter(bookingid=bookingid)
        product = tblbooking.objects.get(bookingid=bookingid)
        return render(request, 'admin/viewpaymentmore.html', {'booking': booking, 'shop': shop, 'product': product})


# View report function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewreport(request):
    return render(request, 'admin/viewreport.html')


# View report by date function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewreportbydate(request):
    return render(request, 'admin/viewreportbydate.html')


# Fill report by date function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def fillreportbydate(request):
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    report = tblpayment.objects.filter(paymentdate__range=(startdate, enddate)).values('paymentamount', 'paymentdate',
                                                                                       'bookingid__productid__productname',
                                                                                       'bookingid__productid__productphoto',
                                                                                       'bookingid')
    return JsonResponse(list(report), safe=False)


# View report by date more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewreportbydatemore(request, id):
    product = tblbooking.objects.get(bookingid=id)
    booking = tblbookingdetails.objects.filter(bookingid=id)
    loginid = product.loginid
    shop = tblshop.objects.get(loginid=loginid)
    return render(request, 'admin/viewreportbydatemore.html', {'booking': booking, 'shop': shop, 'product': product})


# View report by product function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewreportbyproduct(request):
    product = tblbookingdetails.objects.select_related('bookingid__productid__categoryid').filter(
        bookingid__bookingstatus="Paid").values(
        'bookingid__productid__productname', 'bookingid__productid__productphoto',
        'bookingid__productid__price', 'bookingid__productid__categoryid__categoryname',
        'bookingid__productid').annotate(
        total_quantity=Sum('bookingquantity')).order_by('-total_quantity')
    return render(request, 'admin/viewreportbyproduct.html', {'product': product})


# View report by product more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewreportbyproductmore(request, id):
    payment = tblpayment.objects.select_related('bookingid__productid').filter(bookingid__productid=id).values(
        'bookingid__loginid__tblshop__shopname', 'bookingid__loginid__tblshop__shopphoto', 'paymentamount',
        'paymentdate', 'bookingid', 'bookingid__loginid')
    return render(request, 'admin/viewreportbyproductmore.html', {'payment': payment})


# View report by shop function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewreportbyshop(request):
    shop = tblbookingdetails.objects.select_related('bookingid__loginid__tblshop__loginid').filter(
        bookingid__bookingstatus="Paid").values(
        'bookingid__loginid__tblshop__shopname', 'bookingid__loginid__tblshop__shopphoto',
        'bookingid__loginid__tblshop__phone', 'bookingid__loginid__tblshop__loginid__email',
        'bookingid__loginid__tblshop__registrationdate', 'bookingid__loginid').annotate(
        total_quantity=Sum('bookingquantity')).order_by('-total_quantity')
    return render(request, 'admin/viewreportbyshop.html', {'shop': shop})


# View report by shop more function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewreportbyshopmore(request, id):
    payment = tblpayment.objects.select_related('bookingid__loginid').filter(bookingid__loginid=id).values(
        'bookingid__productid__productname', 'bookingid__productid__productphoto', 'paymentamount', 'paymentdate',
        'bookingid', 'bookingid__loginid')
    return render(request, 'admin/viewreportbyshopmore.html', {'payment': payment})


# pie chart

def pie_chart(request):
    labels = []
    data = []

    queryset = tblbookingdetails.objects.select_related('bookingid__productid__categoryid').filter(
        bookingid__bookingstatus="Paid").values(
        'bookingid__productid__productname', 'bookingid__productid__productphoto',
        'bookingid__productid__price', 'bookingid__productid__categoryid__categoryname',
        'bookingid__productid').annotate(
        total_quantity=Sum('bookingquantity'))
    for s in queryset:
        labels.append(s['bookingid__productid__productname'])
        data.append(s['total_quantity'])

    return render(request, 'admin/piechart.html', {
        'labels': labels,
        'data': data,
    })


# Delete district function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletedistrict(request, id):
    district = tbldistrict.objects.get(
        districtid=id)  # To delete a record in a table, start by getting the record you want to delete:
    district.delete()  # call delete() function to perform delete operation
    return viewdistrict(request)


# Delete material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletematerial(request, id):
    material = tblmaterial.objects.get(
        materialid=id)  # To delete a record in a table, start by getting the record you want to delete:
    material.delete()  # call delete() function to perform delete operation
    return viewmaterial(request)


# Delete color function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecolor(request, id):
    color = tblcolor.objects.get(
        colorid=id)  # To delete a record in a table, start by getting the record you want to delete:
    color.delete()  # call delete() function to perform delete operation
    return viewcolor(request)


# Delete location function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletelocation(request, id):
    location = tbllocation.objects.get(
        locationid=id)  # To delete a record in a table, start by getting the record you want to delete:
    location.delete()  # call delete() function to perform delete operation
    return viewlocation(request)


# Delete category function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletecategory(request, id):
    category = tblcategory.objects.get(
        categoryid=id)  # To delete a record in a table, start by getting the record you want to delete:
    category.delete()  # call delete() function to perform delete operation
    return viewcategory(request)


# Delete size function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletesize(request, id):
    size = tblsize.objects.get(
        sizeid=id)  # To delete a record in a table, start by getting the record you want to delete:
    size.delete()  # call delete() function to perform delete operation
    return viewsize(request)


# Delete sub material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletesubmaterial(request, id):
    submaterial = tblsubmaterial.objects.get(
        submaterialid=id)  # To delete a record in a table, start by getting the record you want to delete:
    submaterial.delete()  # call delete() function to perform delete operation
    return viewsubmaterial(request)


# Delete product function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteproduct(request, id):
    product = tblproduct.objects.get(
        productid=id)  # To delete a record in a table, start by getting the record you want to delete:
    product.delete()  # call delete() function to perform delete operation
    return viewproduct(request)


# Delete shop function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteshop(request, id):
    shop = tbllogin.objects.get(loginid=id)
    shop.delete()
    return viewshop(request)


# Delete pattern function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletepattern(request, id):
    pattern = tblpattern.objects.get(
        patternid=id)  # To delete a record in a table, start by getting the record you want to delete:
    pattern.delete()  # call delete() function to perform delete operation
    return viewpattern(request)


# Delete booking function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletebooking(request, id):
    booking = tblbooking.objects.get(
        bookingid=id)  # To delete a record in a table, start by getting the record you want to delete:
    if booking.bookingstatus == 'Confirmed':
        return HttpResponse(
            "<script>alert('Confirmation already done, cannot perform cancellation');window.location='/admin/viewbooking';</script>")
    elif booking.bookingstatus == 'Paid':
        return HttpResponse(
            "<script>alert('Payment already done, cannot perform cancellation');window.location='/admin/viewbooking';</script>")
    else:
        booking.delete()  # call delete() function to perform delete operation
        return viewbooking(request)


# Edit district function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editdistrict(request, id):
    if request.method == 'POST':
        districtname = request.POST.get('districtname')
        districtobj = tbldistrict.objects.get(districtid=id)
        districtobj.districtname = districtname
        districtobj.save()
        return viewdistrict(request)
    else:
        district = tbldistrict.objects.get(districtid=id)
        return render(request, 'admin/editdistrict.html', {'district': district})


# Edit material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editmaterial(request, id):
    if request.method == 'POST':
        materialtype = request.POST.get('materialtype')
        materialobj = tblmaterial.objects.get(materialid=id)
        materialobj.materialtype = materialtype
        materialobj.save()
        return viewmaterial(request)
    else:
        material = tblmaterial.objects.get(materialid=id)
        return render(request, 'admin/editmaterial.html', {'material': material})


# Edit color function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editcolor(request, id):
    if request.method == 'POST':
        colorname = request.POST.get('colorname')
        colorobj = tblcolor.objects.get(colorid=id)
        colorobj.colorname = colorname
        colorobj.save()
        return viewcolor(request)
    else:
        color = tblcolor.objects.get(colorid=id)
        return render(request, 'admin/editcolor.html', {'color': color})


# Edit location function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editlocation(request, id):
    if request.method == 'POST':
        districtid = tbldistrict.objects.get(districtid=request.POST.get('districtid'))
        locationname = request.POST.get('locationname')
        locationobj = tbllocation.objects.get(locationid=id)
        locationobj.locationname = locationname
        locationobj.districtid = districtid
        locationobj.save()
        return viewlocation(request)
    else:
        district = tbldistrict.objects.all()
        location = tbllocation.objects.get(locationid=id)
        return render(request, 'admin/editlocation.html', {'location': location, 'district': district})


# Edit category function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editcategory(request, id):
    if request.method == 'POST':
        categoryname = request.POST.get('categoryname')
        categoryobj = tblcategory.objects.get(categoryid=id)
        categoryobj.categoryname = categoryname
        if len(request.FILES) == 0:
            categoryobj.categoryphoto = request.POST.get('categoryphoto')
        else:
            categoryobj.categoryphoto = request.FILES['categoryimage']
        categoryobj.save()
        return viewcategory(request)
    else:
        category = tblcategory.objects.get(categoryid=id)
        return render(request, 'admin/editcategory.html', {'category': category})


# Edit size function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editsize(request, id):
    if request.method == 'POST':
        productid = tblproduct.objects.get(productid=request.POST.get('productid'))
        sizename = request.POST.get('sizename')
        materialquantity = request.POST.get('materialquantity')
        sizeobj = tblsize.objects.get(sizeid=id)
        sizeobj.productid = productid
        sizeobj.sizename = sizename
        sizeobj.materialquantity = materialquantity
        sizeobj.save()
        return viewsize(request)
    else:
        category = tblcategory.objects.all()
        size = tblsize.objects.get(sizeid=id)
        return render(request, 'admin/editsize.html', {'category': category, 'size': size})


# Edit sub material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editsubmaterial(request, id):
    if request.method == 'POST':
        materialid = tblmaterial.objects.get(materialid=request.POST.get('materialid'))
        submaterialtype = request.POST.get('submaterialtype')
        submaterialobj = tblsubmaterial.objects.get(submaterialid=id)
        submaterialobj.submaterialtype = submaterialtype
        submaterialobj.materialid = materialid
        submaterialobj.save()
        return viewsubmaterial(request)
    else:
        material = tblmaterial.objects.all()
        submaterial = tblsubmaterial.objects.get(submaterialid=id)
        return render(request, 'admin/editsubmaterial.html', {'submaterial': submaterial, 'material': material})


# Edit product  function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editproduct(request, id):
    if request.method == 'POST':
        productname = request.POST.get('productname')
        price = request.POST.get('price')
        description = request.POST.get('description')
        categoryid = tblcategory.objects.get(categoryid=request.POST.get('categoryid'))
        patternid = tblpattern.objects.get(patternid=request.POST.get('patternid'))
        productobj = tblproduct.objects.get(productid=id)
        productobj.productname = productname
        productobj.price = price
        productobj.description = description
        productobj.categoryid = categoryid
        productobj.patternid = patternid
        if len(request.FILES) == 0:
            productobj.productphoto = request.POST.get('productphoto')
        else:
            productobj.productphoto = request.FILES['productimage']
        productobj.save()
        return viewproduct(request)
    else:
        category = tblcategory.objects.all()
        material = tblmaterial.objects.all()
        product = tblproduct.objects.get(productid=id)
        return render(request, 'admin/editproduct.html',
                      {'product': product, 'category': category, 'material': material})


# Edit pattern  function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editpattern(request, id):
    if request.method == 'POST':
        patternname = request.POST.get('patternname')
        submaterialid = tblsubmaterial.objects.get(submaterialid=request.POST.get('submaterialid'))
        patternobj = tblpattern.objects.get(patternid=id)
        patternobj.patternname = patternname
        patternobj.submaterialid = submaterialid
        if len(request.FILES) == 0:
            patternobj.patternphoto = request.POST.get('patternphoto')
        else:
            patternobj.patternphoto = request.FILES['patternimage']
        patternobj.save()
        return viewpattern(request)
    else:
        material = tblmaterial.objects.all()
        pattern = tblpattern.objects.get(patternid=id)
        return render(request, 'admin/editpattern.html',
                      {'material': material, 'pattern': pattern})


# Confirm booking function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def confirmbooking(request, id):
    booking = tblbooking.objects.get(bookingid=id)
    if booking.bookingstatus == 'Requested':
        productid = booking.productid.productid
        email = booking.loginid.email
        product = tblproduct.objects.get(productid=productid)
        patternid = product.patternid.patternid
        bookingdetails = tblbookingdetails.objects.filter(bookingid=id)
        for obj in bookingdetails:
            colorid = obj.colorid.colorid
            materialquantity = obj.sizeid.materialquantity
            totalquantity = obj.bookingquantity * materialquantity
            try:
                stock = tblstock.objects.get(patternid=patternid, colorid=colorid)
            except Exception as e:
                return HttpResponse(
                    "<script>alert('Please purchase stock.');window.location='/admin/purchase';</script>")
            stock.stockquantity = stock.stockquantity - totalquantity
            if stock.stockquantity < 0:
                return HttpResponse(
                    "<script>alert('Out of stock.');window.location='/admin/purchase';</script>")

            msg = EmailMessage()
            variable_name = booking.productid.productname
            msg.set_content(f'Your request for product {variable_name} is approved')
            msg['Subject'] = "Request Approval from Garment Hub"
            msg['from'] = 'jibinbiju308@gmail.com'
            msg['To'] = {email}
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('jibinbiju308@gmail.com', 'xwmtrcbutfhfirae')
                smtp.send_message(msg)

            stock.save()
        booking.bookingstatus = 'Confirmed'
        booking.save()
        return viewbooking(request)
    elif booking.bookingstatus == 'Confirmed':
        return HttpResponse(
            "<script>alert('Confirmation already done.');window.location='/admin/viewbooking';</script>")
    else:
        return HttpResponse("<script>alert('Payment already done.');window.location='/admin/viewbooking';</script>")
