from django.contrib import admin
from .models import User
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):

    list_display = ('email', 'first_name', 'username', 'role') # ---> use is to display custom fields in admin panel
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)