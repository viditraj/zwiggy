from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django import forms
from accounts.utils import detectUser, send_email
from vendor.forms import VendorForm
from .forms import UserForms
from .models import User, UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from orders.models import Order
from django.template.defaultfilters import slugify
import datetime
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
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered and logged in')
        return redirect('custDashboard')
    elif request.method == 'POST':
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

            #Send Verification mail
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered successfully.')
            return redirect('registerUser')
    else:
        form = UserForms()
    context = {  
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already registered and logged in')
        return redirect('vendorDashboard')
    elif request.method == 'POST':
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
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            print('added vendor')
             #Send Verification mail
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_email(request, user, mail_subject, email_template)
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


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congrats, your account is activated')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

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
    user_profile = get_object_or_404(UserProfile, user = request.user)
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    recent_orders = orders[:5]
    context = {
        'orders': orders,
        'recent_orders': recent_orders,
        'orders_count': orders.count(),
        'user_profile':user_profile,
    }
    return render(request, 'accounts/custDashboard.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    recent_orders = orders[:5]

    current_month = datetime.datetime.now().month
    current_month_orders = Order.objects.filter(vendors__in=[vendor.id], created_at__month=current_month)
    current_month_revenue =0
    for i in current_month_orders:
        current_month_revenue += i.get_total_by_vendor()['grand_total']

    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']


    context = {
        'orders': orders,
        'orders_count': orders.count(),
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'current_month_revenue': current_month_revenue,
    }
    return render(request, 'accounts/vendorDashboard.html', context)



def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send password reset email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset link sent to your email')
            return redirect('login')
        else:
            messages.error(request, 'Account with this mail does not exist ')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')

            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')