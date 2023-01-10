from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django import forms
from accounts.utils import detectUser
from vendor.forms import VendorForm
from .forms import UserForms
from .models import User, UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

# Create your views here.

# Restrict customer from accessing vendor page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restrict vendor from accessing customer page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

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
    print('in vendor')
    if request.method == 'POST':
        print('post vendor')
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
            print('added vendor')
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


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Uing in-built django authentication method to authenticate user
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials, try again!')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'you are logged out')
    return redirect('login')


@login_required(login_url='login')

def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request, 'accounts/vendorDashboard.html')