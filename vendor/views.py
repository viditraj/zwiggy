from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from django.contrib import messages
from marketplace.views import is_ajax
from menu.forms import CategoryForm, FoodItemForm
from menu.models import Category, FoodItem
from orders.models import Order, OrderedFood
from vendor.forms import OrderStatusForm, VendorForm, OpeningHourForm
from vendor.models import Images, OpeningHour, Vendor
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.views import check_role_vendor
from django.template.defaultfilters import slugify
import simplejson as json
from accounts.utils import detectUser, send_notification_email
# Create your views here.


def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Settings updated')
            return redirect('vprofile')
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vprofile.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories' : categories,
    }
    return render(request, 'vendor/menu_builder.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor, category=category)
    for item in fooditems:
        print("item.rating")
    context = {
        'fooditems': fooditems,
        'category': category
    }
    return render(request, 'vendor/fooditems_by_category.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug =slugify(category_name)+'-'+str(category.id)
            form.save()
            messages.success(request, 'Category added successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm()
    context = {
        'form':form
    }
    return render(request, 'vendor/add_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug =slugify(category_name)+'-'+str(category.id)
            form.save()
            messages.success(request, 'Category updated successfully')
            return redirect('menu_builder')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form':form,
        'category':get_object_or_404(Category, pk=pk)
    }
    return render(request, 'vendor/edit_category.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    Category.delete(category)
    messages.success(request, 'Category has been deleted successfully')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            fooditem = form.save(commit=False)
            fooditem.vendor = get_vendor(request)
            fooditem.slug =slugify(food_title)+'-'+str(fooditem.id)
            form.save()
            messages.success(request, 'Food Item added successfully')
            return redirect('fooditems_by_category', fooditem.category.id)
    else:
        form = FoodItemForm()
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form' : form,
    }
    return render(request, 'vendor/add_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug =slugify(food_title)
            form.save()
            messages.success(request, 'Food item updated successfully')
            return redirect('fooditems_by_category', food.category.id)
    else:
        form = FoodItemForm(instance=food)
        form.fields['category'].queryset = Category.objects.filter(vendor=get_vendor(request))
    context = {
        'form':form,
        'food':get_object_or_404(FoodItem, pk=pk)
    }
    return render(request, 'vendor/edit_food.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request, pk=None):
    food = get_object_or_404(FoodItem, pk=pk)
    FoodItem.delete(food)
    messages.success(request, 'Food Item has been deleted successfully')
    return redirect('fooditems_by_category', food.category.id)


def opening_hours(request):
    opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form': form,
        'opening_hours': opening_hours,
    }
    return render(request, 'vendor/opening_hours.html', context)


def add_opening_hours(request):
    if request.user.is_authenticated:
        if is_ajax(request) and request.method == 'POST':
            day = request.POST.get('day')
            from_hour = request.POST.get('from_hour')
            to_hour = request.POST.get('to_hour')
            is_closed = request.POST.get('is_closed')
            try:
                hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)
                if hour:
                    day  = OpeningHour.objects.get(id=hour.id)
                    if day.is_closed:
                        response = {'status':'success', 'id':hour.id, 'day':day.get_day_display(),'is_closed':'closed'}
                    else:
                        response = {'status':'success', 'id':hour.id, 'day':day.get_day_display(), 'from_hour':hour.from_hour, 'to_hour':hour.to_hour}
                return JsonResponse(response)
            except IntegrityError as e:
                response = {'status':'failed', 'message': from_hour+'-'+to_hour+' already exists for this day'}
                return JsonResponse(response)
        else:
            HttpResponse('Invalid Request')


def remove_opening_hours(request, pk=None):
    if request.user.is_authenticated:
        if is_ajax(request):
            hour = get_object_or_404(OpeningHour, pk=pk)
            hour.delete()
            return JsonResponse({'status':'success', 'id': pk})


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFood.objects.filter(order=order, fooditem__vendor=get_vendor(request))
        vendor_name = get_vendor(request).vendor_name
        context = {
            'subtotal': order.get_total_by_vendor()['subtotal'],
            'order': order,
            'ordered_food': ordered_food,
            'tax_data': order.get_total_by_vendor()['tax_dict'],
            'grand_total': order.get_total_by_vendor()['grand_total'],
            'vendor_name': vendor_name,
        }
    except Exception as e:
        print(e)
        return redirect('vendor')
    return render(request, 'vendor/order_detail.html', context)


def my_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    orders = Order.objects.filter(vendors__in=[vendor.id], is_ordered=True).order_by('created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'vendor/my_orders.html', context )


def change_order_status(request, order_number):
    order = Order.objects.get(order_number=order_number, is_ordered=True)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            delivery_time = form.cleaned_data['delivery_time']
            form.save()
            status = form.cleaned_data['status']
            if status == 'Accepted':
                mail_subject = 'Your Order is being processed.'
            elif status == 'Completed':
                mail_subject = 'Your Order is delivered successfully.'
            elif status == 'Cancelled':
                mail_subject = 'Your Order is cancelled.'
            mail_template = 'orders/order_processing_email.html'
            context = {
            'first_name': order.first_name,
            'last_name' : order.last_name,
            'to_email': order.email,
            'delivery_time' : delivery_time,
            'status': status,
            }
            send_notification_email(mail_subject, mail_template, context)
            messages.success(request, 'Order Status Updated Successfully')
            return redirect('vendor_my_orders')
    else:
        form = OrderStatusForm(instance = order)
    context = {
        'form' : form,
        'order': order,
    }
    return render(request, 'vendor/change_order_status.html', context)


def add_images(request):
    vendor = Vendor.objects.get(user=request.user)
    images = Images.objects.filter(vendor=vendor)
    context={
        'images':images,
        'vendor':vendor,
    }
    return render(request, 'vendor/add_images.html', context)


def upload_images(request):
    vendor = Vendor.objects.get(user=request.user)
    if request.method == "POST":
        images = request.FILES.getlist('up_images')
        for image in images:
            Images.objects.create(image=image, vendor=vendor )
        messages.success(request, 'Images uploaded Successfully')
        return redirect('add_images')
    else:
        images = Images.objects.filter(vendor=vendor)
        context={
        'images':images,
        'vendor':vendor,
        }
        return render(request, 'vendor/add_images.html', context)

def remove_images(request, pk=None):
    if request.user.is_authenticated:
        if is_ajax(request):
            image = get_object_or_404(Images, pk=pk)
            image.delete()
            return JsonResponse({'status':'success', 'id': pk})
