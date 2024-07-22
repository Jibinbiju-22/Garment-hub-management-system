from django.http import HttpResponse
from django.shortcuts import render
from adminapp.models import *
from customerapp.models import *
from django.db.models import Q
from django.views.decorators.cache import cache_control



# Create your views here.

# Home function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    loginid = request.session.get('loginid')
    category = tblcategory.objects.all()
    booking = tblbooking.objects.filter(loginid=loginid)
    paid = tblbooking.objects.filter(loginid=loginid, bookingstatus='Paid')
    data = tblshop.objects.filter(loginid=loginid)
    bookingall = tblbooking.objects.filter(
        Q(loginid=loginid) & (Q(bookingstatus='Requested') | Q(bookingstatus='Confirmed')))
    booking = tblbooking.objects.filter(loginid=loginid).order_by('bookingid').last()

    return render(request, 'shop/home.html',
                  {'data': data, 'loginid': loginid, 'booking': booking, 'bookingall': bookingall, 'paid': paid,
                   'category': category})


# View category function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewcategory(request):
    category = tblcategory.objects.all()
    material = tblmaterial.objects.all()
    return render(request, 'shop/viewcategory.html', {'category': category, 'material': material})


# View product function
from collections import Counter

from .preprocessing import preprocess_search_query
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def viewproduct(request):
    product = tblproduct.objects.all()
    loginid = request.session.get('loginid')
    shop = tblshop.objects.get(loginid=loginid)
    shopid = tblshop.objects.get(shopid=shop.shopid)

    # Retrieve the search history queryset and extract the 'query' field
    search_history_queries = shopid.searchhistory_set.values_list('query', flat=True)

    # Preprocess the search history queries
    preprocessed_search_history = preprocess_search_query(search_history_queries)

    # Placeholder for generating recommendations based on preprocessed search history
    recommended_product_ids = generate_recommendations(preprocessed_search_history)
    # Convert the list of recommended product IDs to a Counter object
    product_id_counts = Counter(recommended_product_ids)

    # Sort the product IDs by their counts in descending order
    sorted_product_ids = sorted(product_id_counts, key=product_id_counts.get, reverse=True)

    # Now sorted_product_ids contains the product IDs sorted by their counts in descending order
    sorted_products = [tblproduct.objects.get(productid=product_id) for product_id in sorted_product_ids]
    sorted_products_info = []
    for product_id in sorted_product_ids:
        productobj = tblproduct.objects.get(productid=product_id)
        product_info = {
            'productname': productobj.productname,
            'description': productobj.description,
            'price': productobj.price,
            'productphoto':productobj.productphoto,
            'productid': productobj.productid,
            # Add other relevant attributes as needed
        }
        sorted_products_info.append(product_info)
    return render(request, 'shop/viewproduct.html', {'product': product, 'sorted_products_info': sorted_products_info})


# View sub material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewsubmaterial(request):
    submaterial = tblsubmaterial.objects.all()
    return render(request, 'shop/viewsubmaterial.html', {'submaterial': submaterial})


# View pattern function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpattern(request):
    pattern = tblpattern.objects.all()
    return render(request, 'shop/viewpattern.html', {'pattern': pattern})


# View product by category function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproductbycategory(request, id):
    category = tblcategory.objects.get(categoryid=id)
    product = tblproduct.objects.filter(categoryid=id)
    return render(request, 'shop/viewproductbycategory.html', {'product': product, 'category': category})


# View product more  function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproductmore(request, id):
    product = tblproduct.objects.get(productid=id)
    return render(request, 'shop/viewproductmore.html', {'product': product})


# View sub material by material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewsubmaterialbymaterial(request, id):
    material = tblmaterial.objects.get(materialid=id)
    submaterial = tblsubmaterial.objects.filter(materialid=id)
    return render(request, 'shop/viewsubmaterialbymaterial.html', {'submaterial': submaterial, 'material': material})


# View pattern by sub material function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpatternbysubmaterial(request, id):
    submaterial = tblsubmaterial.objects.get(submaterialid=id)
    pattern = tblpattern.objects.filter(submaterialid=id)
    return render(request, 'shop/viewpatternbysubmaterial.html', {'pattern': pattern, 'submaterial': submaterial})


# View product by pattern function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewproductbypattern(request, id):
    pattern = tblpattern.objects.get(patternid=id)
    product = tblproduct.objects.filter(patternid=id)
    return render(request, 'shop/viewproductbypattern.html', {'pattern': pattern, 'product': product})


# View profile function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewprofile(request, id):
    shop = tblshop.objects.filter(loginid=id)
    return render(request, 'shop/viewprofile.html', {'shop': shop})


# View booking function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewbookingbyshop(request, id):
    booking = tblbooking.objects.get(bookingid=id)
    bookingdetails = tblbookingdetails.objects.filter(bookingid=id)
    # Initialize sum variable
    bookingamount = 0

    # Loop through each object and add the value of the specific column to the sum
    for obj in bookingdetails:
        # Assuming 'column_name' is the name of the column you want to sum
        bookingamount += obj.bookingamount
    return render(request, 'shop/viewbookingbyshop.html',
                  {'bookingamount': bookingamount, 'booking': booking, 'bookingdetails': bookingdetails})


# View all bookings function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewbookingall(request):
    loginid = request.session.get('loginid')
    booking = tblbooking.objects.filter(
        Q(loginid=loginid) & (Q(bookingstatus='Requested') | Q(bookingstatus='Confirmed')))
    return render(request, 'shop/viewbookingall.html', {'booking': booking})


# View payment function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpayment(request):
    loginid = request.session.get('loginid')
    paid = tblbooking.objects.filter(loginid=loginid, bookingstatus='Paid')
    return render(request, 'shop/viewpayment.html', {'paid': paid})


# View payment function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def viewpaymentbyshop(request, id):
    booking = tblbooking.objects.get(bookingid=id)
    payment = tblpayment.objects.get(bookingid=id)
    bookingdetails = tblbookingdetails.objects.filter(bookingid=id)
    return render(request, 'shop/viewpaymentbyshop.html',
                  {'booking': booking, 'bookingdetails': bookingdetails, 'payment': payment})


# Edit profile function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def editprofile(request, id):
    if request.method == 'POST':
        shopname = request.POST.get('shopname')
        if len(request.FILES) == 0:
            shopphoto = request.POST.get('shopphoto')
        else:
            shopphoto = request.FILES['shopimage']
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        locationid = tbllocation.objects.get(locationid=request.POST.get('locationid'))
        email = request.POST.get('email')


        loginobj = tbllogin.objects.get(loginid=id)
        loginobj.email = email

        loginobj.save()

        shopobj = tblshop.objects.get(loginid=id)
        shopobj.shopname = shopname
        shopobj.shopphoto = shopphoto
        shopobj.address = address
        shopobj.phone = phone
        shopobj.locationid = locationid
        shopobj.save()

        return viewprofile(request, id)

    else:
        district = tbldistrict.objects.all()
        shop = tblshop.objects.filter(loginid=id)
        return render(request, 'shop/editprofile.html', {'district': district, 'shop': shop})


# Booking function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def booking(request, id):
    if request.method == 'POST':
        productid = tblproduct.objects.get(productid=id)
        loginid = request.session.get('loginid')
        deliverydate = request.POST.get('deliverydate')
        bookingstatus = 'Requested'

        bookingobj = tblbooking()
        bookingobj.productid = productid
        bookingobj.loginid = tbllogin.objects.get(loginid=loginid)
        bookingobj.deliverydate = deliverydate
        bookingobj.bookingstatus = bookingstatus
        bookingobj.save()

        return HttpResponse("<script>window.location='/shop/bookingdetails';</script>")

    else:
        product = tblproduct.objects.get(productid=id)
        return render(request, 'shop/booking.html', {'product': product})


# Booking details function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def bookingdetails(request):
    if request.method == 'POST':
        booking = tblbooking.objects.last()
        bookingid = booking.bookingid
        sizeid = request.POST.get('sizeid')
        bookingquantity = request.POST.get('bookingquantity')
        bookingamount = request.POST.get('bookingamount')
        colorid = request.POST.get('colorid')
        bookingdetailsobj = tblbookingdetails()
        if tblbookingdetails.objects.filter(colorid=colorid, sizeid=sizeid,bookingid=bookingid).exists():
            bookingdetails = tblbookingdetails.objects.get(colorid=colorid, sizeid=sizeid,bookingid=bookingid)
            bookingdetails.bookingamount = int(bookingdetails.bookingamount) + int(bookingamount)
            bookingdetails.bookingquantity = int(bookingdetails.bookingquantity) + int(bookingquantity)
            bookingdetails.save()
            return HttpResponse("<script>alert('Request added..');window.location='/shop/bookingdetails';</script>")
        else:
            bookingdetailsobj.bookingquantity = bookingquantity
            bookingdetailsobj.bookingamount = bookingamount
            bookingdetailsobj.colorid = tblcolor.objects.get(colorid=colorid)
            bookingdetailsobj.sizeid = tblsize.objects.get(sizeid=sizeid)
            bookingdetailsobj.bookingid = tblbooking.objects.get(bookingid=bookingid)
            bookingdetailsobj.save()
            return HttpResponse("<script>alert('Request added..');window.location='/shop/bookingdetails';</script>")
    else:
        booking = tblbooking.objects.last()
        productid = booking.productid.productid
        size = tblsize.objects.filter(productid=productid)
        color = tblcolor.objects.all()

        bookingid = booking.bookingid
        data = tblbookingdetails.objects.filter(bookingid=bookingid)
        sum = 0
        for item in data:
            sum += item.bookingamount
        return render(request, 'shop/bookingdetails.html',
                      {'booking': booking, 'color': color, 'size': size, 'sum': sum})


# Payment function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment(request, id):
    if request.method == 'POST':
        paymentamount = request.POST.get('paymentamount')
        paymentobj = tblpayment()
        paymentobj.bookingid = tblbooking.objects.get(bookingid=id)
        paymentobj.paymentamount = paymentamount
        if tblpayment.objects.filter(bookingid=id).exists():
            return HttpResponse(
                "<script>alert('Payment already done');window.location='/shop/home';</script>")
        else:
            paymentobj.save()
            bookingobj = tblbooking.objects.get(bookingid=id)
            bookingobj.bookingstatus = 'Paid'
            bookingobj.save()
            return HttpResponse("<script>alert('Payment successful.');window.location='/shop/home';</script>")
    else:
        booking = tblbooking.objects.get(bookingid=id)
        if booking.bookingstatus == 'Confirmed':
            bookingdetails = tblbookingdetails.objects.filter(bookingid=id)
            # Initialize sum variable
            bookingamount = 0

            # Loop through each object and add the value of the specific column to the sum
            for obj in bookingdetails:
                # Assuming 'column_name' is the name of the column you want to sum
                bookingamount += obj.bookingamount
            return render(request, 'shop/payment.html', {'bookingamount': bookingamount})
        elif booking.bookingstatus == 'Paid':
            return HttpResponse(
                "<script>alert('Payment already done');window.location='/shop/home';</script>")
        else:
            return HttpResponse(
                "<script>alert('Request not accepted.');window.location='/shop/viewbookingall';</script>")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    if 'search' in request.GET:
        query = request.GET['search']
        # Perform a search query on the database table
        product = tblproduct.objects.filter(productname__icontains=query)
        loginid = request.session.get('loginid')
        shop = tblshop.objects.get(loginid=loginid)
        shopid = tblshop.objects.get(shopid=shop.shopid)
        # return HttpResponse(shopid)
        SearchHistory.objects.create(shopid=shopid, query=query)
        return render(request, 'shop/viewproductbysearch.html', {'query': query, 'product': product})
    else:
        return HttpResponse("No search query provided.")


# from .preprocessing import preprocess_search_query
# def show_recommendations(request):
#     preprocessed_search_history = preprocess_search_query(request.user.searchhistory_set.values_list('query', flat=True))
#     # Your recommendation generation code here
#     return render(request, 'recommendations.html', {'recommendations': recommendations})

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.http import JsonResponse


def generate_recommendations(preprocessed_search_history):
    if not preprocessed_search_history:
        # Handle the case where there are no search histories
        return []
    # Fetch product descriptions from the database
    products = tblproduct.objects.only('productid', 'description')

    # Convert preprocessed search history into TF-IDF vectors
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(preprocessed_search_history)

    # Convert product descriptions into TF-IDF vectors
    product_descriptions = [product.description for product in products]
    product_tfidf_matrix = tfidf_vectorizer.transform(product_descriptions)

    # Compute similarity scores between search history and products
    cosine_similarities = linear_kernel(tfidf_matrix, product_tfidf_matrix)

    # Get indices of top recommendations
    num_recommendations = min(5, len(products))
    top_indices = cosine_similarities.argsort()[:, :-num_recommendations - 1:-1].tolist()  # Convert to list

    # return JsonResponse({'top_indices': top_indices})
    # Ensure that top_indices is properly structured
    print(top_indices)

    # Get recommended product IDs
    recommended_product_ids = [products[int(sublist[0])].productid for sublist in top_indices]

    return recommended_product_ids

def changepassword(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        newpassword = request.POST.get("newpassword")
        confirmpassword = request.POST.get("confirmpassword")
        if tbllogin.objects.filter(email=email, password=password).exists():
            lo = tbllogin.objects.get(email=email, password=password)
            if newpassword == confirmpassword:
                lo.password = newpassword
                lo.save()
                return HttpResponse("<script>alert('Successfully updated!!');window.location='/shop/home'</script>")
            return HttpResponse("<script>alert('Password mismatch!!');window.location='/shop/changepassword'</script>")
        return HttpResponse("<script>alert('Invalid email or password!!');window.location='/shop/changepassword'</script>")
    return render(request, "shop/changepassword.html")

