from django.contrib import admin
from vendor.models import Images, Vendor
from vendor.models import OpeningHour

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name','rating', 'is_approved','created_at')
    list_display_links = ('user', 'vendor_name')
    list_editable = ('is_approved',)

class OpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hour', 'to_hour')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'image')

admin.site.register(Images, ImageAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(OpeningHour, OpeningHourAdmin)
