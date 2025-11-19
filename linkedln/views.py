from django.shortcuts import render,HttpResponse,redirect
from.models import*
from.models import CartItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.urls import reverse

# Create your views here.
def fruitss(request):
    d = fruits.objects.all()
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
        itmm = Wishlist.objects.filter(user=request.user).count()
    else:
        itm = 0
        itmm = 0

    return render(request, 'index.html', {'p': d, 'itm': itm, 'itmm': itmm})

def vegetables(request):
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
    else:
        itm = 0
    return render(request, 'shop.html', {'itm': itm})

def wishlist(request):
    Wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html')

def product(request,id):
    dd = fruits.objects.get(id=id)
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
        itmm = Wishlist.objects.filter(user=request.user).count()
    else:
        itm = 0
        itmm = 0
    if request.method=='POST':
        # Ensure only authenticated users can create cart items
        if not request.user.is_authenticated:
            # redirect to login page if anonymous tries to add to cart; after login send back to product page
            login_url = reverse('login')
            product_url = reverse('product_detail', args=[id])
            return redirect(f"{login_url}?next={product_url}")
        qty=int(request.POST['quantity'])
        a = CartItem(fruits=dd, quantity=qty, user=request.user)
        a.save()
        return redirect(cart)
        
    return render(request,'product-single.html',{'dd':dd,'itm':itm,'itmm':itmm})

def cart(request):
    # Require login to view cart
    if not request.user.is_authenticated:
        login_url = reverse('login')
        return redirect(f"{login_url}?next={reverse('cart')}")
    
    cart_items = CartItem.objects.filter(user=request.user)
    itm = CartItem.objects.filter(user=request.user).count()
    total_price = sum(item.fruits.price * item.quantity for item in cart_items)
    
    if request.user.is_authenticated:
        itmm = Wishlist.objects.filter(user=request.user).count()
    else:
        itmm = 0
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'itm': itm, 'itmm': itmm})


def checkouts(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname=request.POST['lname']
        zip=request.POST['zip']
        emailaddress=request.POST['email']
        phone=request.POST['phone']
        obj=CartItem.objects.filter(user=request.user)
        for i in obj:
            BillingDetails(firstname=fname,lastname=lname,zip=zip,emailaddress=emailaddress,phone=phone,cart_id=i,user=request.user).save()  
            obj.delete()
            return HttpResponse("your order placed! Thank you")

    return render(request,'checkout.html')

def about(request):
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
    else:
        itm = 0
    return render(request, 'about.html', {'itm': itm})

def blog(request):
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
    else:
        itm = 0
    return render(request, 'blog.html', {'itm': itm})

# def blog_single(request):
#     """Render a single blog post page (static template for now)."""
#     if request.user.is_authenticated:
#         itm = CartItem.objects.filter(user=request.user).count()
#     else:
#         itm = 0
#     return render(request, 'blog-single.html', {'itm': itm})
# 
def blogsingle(request):
    """Render a single blog post page (static template for now)."""
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
    else:
        itm = 0
    
    # Debug information
    print("DEBUG: Rendering blog-single.html")
    print(f"DEBUG: User authenticated: {request.user.is_authenticated}")
    print(f"DEBUG: Cart items: {itm}")
    
    return render(request, 'blog-single.html', {'itm': itm})
def contact(request):
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
    else:
        itm = 0
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        subject=request.POST['subject']
        cnt(name=name,email=email,message=message,subject=subject).save()
        return HttpResponse("Message sent successfully")
    return render(request, 'contact.html', {'itm': itm})

def remove_form_cart(request,id):
    # Require login to remove from cart
    if not request.user.is_authenticated:
        login_url = reverse('login')
        return redirect(f"{login_url}?next={reverse('cart')}")
    
    cart_item = CartItem.objects.get(id=id, user=request.user)
    cart_item.delete()
    return redirect(cart)
    # return HttpResponse("item remove")



def add_to_wishlist(request, id):
    # Ensure only authenticated users can add to wishlist
    if not request.user.is_authenticated:
        login_url = reverse('login')
        product_url = reverse('product_detail', args=[id])
        return redirect(f"{login_url}?next={product_url}")
    
    products = get_object_or_404(fruits, id=id)
    # Check if already in wishlist
    existing_wishlist = Wishlist.objects.filter(user=request.user, product=products).first()
    if not existing_wishlist:
        Wishlist(user=request.user, product=products).save()
    
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return redirect('wishlist_view')

def wishlist_view(request):
    # Require login to view wishlist
    if not request.user.is_authenticated:
        login_url = reverse('login')
        return redirect(f"{login_url}?next={reverse('wishlist_view')}")
    
    wishlist_items = Wishlist.objects.filter(user=request.user)
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
        itmm = Wishlist.objects.filter(user=request.user).count()
    else:
        itm = 0
        itmm = 0
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items, 'itm': itm, 'itmm': itmm})

def shop(request):
    d = fruits.objects.all()
    if request.user.is_authenticated:
        itm = CartItem.objects.filter(user=request.user).count()
        itmm = Wishlist.objects.filter(user=request.user).count()
    else:
        itm = 0
        itmm = 0
    return render(request, 'shop.html', {'p': d, 'itm': itm, 'itmm': itmm})


def remove_from_wishlist(request,id):
    # Require login to remove from wishlist
    if not request.user.is_authenticated:
        login_url = reverse('login')
        return redirect(f"{login_url}?next={reverse('wishlist_view')}")
    
    item = Wishlist.objects.filter(id=id, user=request.user)
    item.delete()
    return redirect(wishlist_view)

# def login(request):
#     if request.method == "POST":
#         user_input = request.POST['user']
#         password = request.POST['password']
#         user_obj = User.objects.filter(username=user_input).first()
#         if not user_obj:
#             user_obj = User.objects.filter(email=user_input).first()
#         if user_obj:
#             user = authenticate(username=user_obj.username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('index')  # Redirect to dashboard after login
#         return HttpResponse("Invalid credentials")
#     return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            # After successful login, respect next parameter if present
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})

    return render(request, 'login.html')




def register(request):
    if request.method=="POST":
        name=request.POST['Username']
        email=request.POST['email']
        phn=request.POST['phn']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        if password==cpassword:
            User.objects.create_user(username=name,email=email,password=password).save()
            return redirect(login)
        else:
            return HttpResponse("Password should be same")

    return render(request,'register.html')

def logout(request):
    auth_logout(request)
    return redirect('index')

# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import login as auth_login
# from django.contrib import messages

# def register(request):
#     if request.method == 'POST':
#         # Use get() method instead of direct access to avoid KeyError
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         # Check if all required fields are provided
#         if not all([username, email, password, confirm_password]):
#             messages.error(request, 'Please fill in all required fields')
#             return render(request, 'register.html')
        
#         if password == confirm_password:
#             try:
#                 user = User.objects.create_user(username, email, password)
#                 auth_login(request, user)
#                 messages.success(request, 'Registration successful!')
#                 return redirect('index')
#             except Exception as e:
#                 messages.error(request, f'Registration failed: {str(e)}')
#         else:
#             messages.error(request, 'Passwords do not match')
    
#     return render(request, 'register.html')

