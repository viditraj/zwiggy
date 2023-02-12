from django.contrib import admin
from .models import VendorReviews
# Register your models here.

class VendorReviewAdmin(admin.ModelAdmin):
    model = VendorReviews
    list_display = ['user', 'vendor', 'content', 'created_at', 'likes' , 'rating_given' ]


admin.site.register(VendorReviews , VendorReviewAdmin)

