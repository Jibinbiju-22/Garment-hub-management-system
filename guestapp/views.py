from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from guestapp.models import *
from adminapp.models import *
from django.views.decorators.cache import cache_control
from django.shortcuts import redirect
import random
import string
from email.message import EmailMessage
import smtplib
# Create your views here.


# login fuction
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if tbllogin.objects.filter(email=email, password=password).exists():
            loginobj = tbllogin.objects.get(email=email, password=password)
            request.session['email'] = loginobj.email
            request.session['loginid'] = loginobj.loginid
            loginid=request.session['loginid']
            role = loginobj.role
            if role == 'admin':
                return HttpResponse(
                    "<script>window.location='/admin/home';</script>")
            elif role == 'shop':
                return HttpResponse(
                    "<script>window.location='/shop/home';</script>")
        else:
            return HttpResponse("<script>alert('Invalid email or password');window.location='/guest/login';</script>")
    else:
        return render(request, 'guest/login.html')

# Shop registration function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if tbllogin.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exist.');window.location='/guest/registration';</script>")
        loginobj = tbllogin()
        loginobj.email = email
        loginobj.password = password
        loginobj.role = 'shop'
        loginobj.loginstatus = 'confirmed'
        if tblshop.objects.filter(phone=phone).exists():
            return HttpResponse("<script>alert('Phone already exist.');window.location='/guest/registration';</script>")
        shopobj = tblshop()
        shopobj.shopname = request.POST.get('shopname')
        shopobj.phone = request.POST.get('phone')
        shopobj.address = request.POST.get('address')
        shopobj.locationid = tbllocation.objects.get(locationid=request.POST.get('locationid'))
        shopobj.shopphoto = request.FILES['shopphoto']
        loginobj.save()
        shopobj.loginid = loginobj
        shopobj.save()
        return HttpResponse("<script>alert('Shop registered');window.location='/guest/login';</script>")
    else:
        district = tbldistrict.objects.all()
        return render(request, 'guest/registration.html', {'district': district})


# Function for fill location data.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def filllocation(request):
    districtid=int(request.POST.get("districtid"))
    location=tbllocation.objects.filter(districtid=districtid).values()
    return JsonResponse(list(location),safe=False)

def logout(request):
    if "loginid" in request.session:
        del request.session["loginid"]
        del request.session['email']
        return redirect('/guest/login')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        if tbllogin.objects.filter(email=email).exists():
            lg = tbllogin.objects.get(email=email)
            lid = lg.loginid
            cust = tblshop.objects.get(loginid=lid)
            email = lg.email
            customer_name = cust.shopname
            characters = string.ascii_letters + string.digits
            random_number = ''.join(random.choice(characters) for _ in range(8))
            # return HttpResponse(random_number)
            lg.password = random_number
            lg.save()
            msg = EmailMessage()
            msg.set_content(f'Hi {customer_name},Your new password to login in is {random_number}')
            msg['Subject'] = "Forgot Password ?"
            msg['from'] = 'jibinbiju308@gmail.com'
            msg['To'] = {email}
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login('jibinbiju308@gmail.com', 'xwmtrcbutfhfirae')
                smtp.send_message(msg)
            return HttpResponse("<script>alert('Login with new password in your email');window.location='/guest/login';</script>")
        return HttpResponse("<script>alert('No data found');window.location='/guest/forgotpassword';</script>")
    return render(request, 'guest/forgotpassword.html')

def home(request):
    return render(request, 'guest/home.html')

