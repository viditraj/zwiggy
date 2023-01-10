from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from vendor.forms import VendorForm
from .forms import UserForms
from .models import User, UserProfile

# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForms(request.POST)
        if form.is_valid():
            # Method 1 to create user
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.save()

            #Method 2 using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password, phone_number=phone_number)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully.')
            return redirect('registerUser')
    else:
        form = UserForms()
    context = {  
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):

    if request.method == 'POST':
        #store the data and create the user
        form = UserForms(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if v_form.is_valid() and form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password, phone_number=phone_number)
            user.role = User.RESTAURANT
            user.save()
            
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered successfully! Please wait for approval.')
            return redirect('registerVendor')
    else:
        form = UserForms()
        v_form = VendorForm()
    context = {  
        'form' : form,
        'v_form' : v_form,
    }
    return render(request, 'accounts/registerVendor.html', context)