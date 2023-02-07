from django.contrib import admin
from .models import Order, OrderedFood, Payment
# Register your models here.

class OrderedFoodInline(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order', 'payment', 'quantity', 'user', 'fooditem', 'price', 'amount')
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method','status', 'order_placed_to', 'is_ordered']
    inlines = [OrderedFoodInline]


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id','payment_method', 'amount', 'status']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderedFood)
