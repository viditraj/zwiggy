from django.shortcuts import render, redirect
from reviews.models import VendorReviews
from vendor.models import Vendor
from django.http import JsonResponse
from .forms import ReviewForm
from django.contrib import messages


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

# Create your views here.
def reviews(request, vendor_slug):
    vendor = Vendor.objects.get(vendor_slug=vendor_slug)
    reviews = VendorReviews.objects.filter(vendor = vendor).order_by('created_at')
    revc = [0,0,0,0,0]
    for review in reviews:
        if review.rating_given ==1:
            revc[0] +=1
        elif review.rating_given ==2:
            revc[1] +=1
        elif review.rating_given ==3:
            revc[2] +=1
        elif review.rating_given ==4:
            revc[3] +=1
        elif review.rating_given ==5:
            revc[4] +=1

    review_dict ={
        '5' : revc[4],
        '4' : revc[3],
        '3' : revc[2],
        '2' : revc[1],
        '1' : revc[0]
        }
    context = {
        'vendor_slug': vendor_slug,
        'vendor': vendor,
        'reviews': reviews,
        'review_dict': review_dict,
    }
    return render(request, 'vendor/reviews.html', context)


