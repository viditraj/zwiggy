from . import  views
from django.urls import path
from accounts import views as AccountViews
urlpatterns = [
    path('',AccountViews.vendorDashboard, name='vendor'),
    path('profile', views.vprofile, name='vprofile'),
    
]