from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home),

    path('viewcategory', views.viewcategory),
    path('viewproduct', views.viewproduct),
    path('viewsubmaterial', views.viewsubmaterial),
    path('viewpattern', views.viewpattern),
    path('viewproductbycategory/<id>', views.viewproductbycategory, name='viewproductbycategory'),
    path('viewproductmore/<id>', views.viewproductmore, name='viewproductmore'),
    path('viewsubmaterialbymaterial/<id>', views.viewsubmaterialbymaterial, name='viewsubmaterialbymaterial'),
    path('viewpatternbysubmaterial/<id>', views.viewpatternbysubmaterial, name='viewpatternbysubmaterial'),
    path('viewproductbypattern/<id>', views.viewproductbypattern, name='viewproductbypattern'),
    path('viewprofile/<id>', views.viewprofile, name='viewprofile'),
    path('viewbookingbyshop/<id>', views.viewbookingbyshop, name='viewbookingbyshop'),
    path('viewbookingall', views.viewbookingall, name='viewbookingall'),
    path('viewpayment', views.viewpayment),
    path('viewpaymentbyshop/<id>', views.viewpaymentbyshop, name='viewpaymentbyshop'),

    path('editprofile/<id>', views.editprofile, name='editprofile'),

    path('booking/<id>', views.booking, name='booking'),
    path('bookingdetails', views.bookingdetails, name='bookingdetails'),
    path('payment/<id>', views.payment, name='payment'),
    path('changepassword', views.changepassword, name='changepassword'),

    path('search', views.search, name='search'),

]
