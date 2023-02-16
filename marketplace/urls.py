from django.urls import path, include
from . import views
from reviews import views as ReviewViews

urlpatterns = [
    path('', views.marketplace, name='marketplace'),
    path('<slug:vendor_slug>/', views.vendor_detail, name='vendor_detail'),
    path('<slug:vendor_slug>/reviews/', include('reviews.urls')),
    path('<slug:vendor_slug>/images/', views.images, name='images'),
    path('add_review/<slug:vendor_slug>/', views.add_review, name='add_review'),
    

    # Add to Cart
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add_to_cart'),

    # Decrease from Cart
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease_cart'),

    # Delete from Cart
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),

] 
