from django.urls import path,include
from django.contrib import admin
from.views import*
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
  
  path('', fruitss, name='index'),
  path('index/', fruitss, name='index_alt'),
  path('vegetables/', vegetables, name='vegetables'),
  path('wishlist/', wishlist, name='wishlist'),
  path('product/<int:id>/', product, name='product_detail'),
  path('remove/<int:id>/', remove_form_cart, name='remove_cart_item'),
  path('cart/', cart, name='cart'),
  path('checkouts/', checkouts, name='checkouts'),
  path('about/', about, name='about'),
  path('blog/', blog, name='blog'),
  path('blog-single/', blogsingle, name='blog_single'),
  path('contacts/', contact, name='contact'),
  path('whislist/<int:id>/', add_to_wishlist, name='add_to_wishlist'),
  path('whislistview/', wishlist_view, name='wishlist_view'),
  path('removew/<int:id>/', remove_from_wishlist, name='remove_from_wishlist'),
  path('login/', login, name='login'),
  path('register/', register, name='register'),
  path('logout/', logout, name='logout'),
  path('shop/', shop, name='shop'),



]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
