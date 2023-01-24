from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .context_processors import get_cart_amounts, get_cart_counter
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from .models import Cart
from django.contrib.auth.decorators import login_required
# Create your views here.


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)[:8]
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
       Prefetch(
            'fooditems',
            queryset= FoodItem.objects.filter(is_available=True)
       )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories': categories,
        'cart_items': cart_items,
    }   
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            # Check if food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # If food exists, check if user has already added that food to cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity as food item already exists
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status': 'success','message': 'Increased the cart quantity', 'cart_counter': get_cart_counter(request), 'qty':checkCart.quantity, 'cart_amount':get_cart_amounts(request)})
                except:
                    # Create new cart as the cart doesnot exists
                    checkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'success','message': 'Added the food to the cart', 'cart_counter': get_cart_counter(request), 'qty':checkCart.quantity,'cart_amount':get_cart_amounts(request)})
            except:
                 return JsonResponse({'status': 'failed', 'message': 'This food item does not exists'})
        else:    
            return JsonResponse({'status': 'failed','message': 'Invalid Request!'})
    else:
        return JsonResponse({'status': 'login_required','message': 'Please login to continue'})



def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            # Check if food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # If food exists, check if user has already added that food to cart
                try:
                    checkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if checkCart.quantity > 1:
                        # Decrease the cart quantity 
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                    return JsonResponse({'status': 'success', 'cart_counter': get_cart_counter(request), 'qty':checkCart.quantity, 'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'failed','message': 'You do not have this item in your cart'})
            except:
                 return JsonResponse({'status': 'failed', 'message': 'This food item does not exists'})
        else:    
            return JsonResponse({'status': 'failed','message': 'Invalid Request!'})
    else:
        return JsonResponse({'status': 'login_required','message': 'Please login to continue'})


def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)

@login_required(login_url= 'login')
def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if is_ajax(request):
            try:
                # Check if cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'success','message': 'Cart item deleted', 'cart_counter': get_cart_counter(request), 'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'failed','message': 'Cart item does not exists'})
        else:
            return JsonResponse({'status': 'failed','message': 'Invalid Request!'})

