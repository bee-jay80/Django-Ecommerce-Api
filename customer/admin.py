from django.contrib import admin
from .models import Customer, Addresses
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')

@admin.register(Addresses)
class AddressesAdmin(admin.ModelAdmin):
    list_display = ('customer', 'address_line1', 'city', 'state', 'country', 'is_default')
    search_fields = ('customer__email', 'address_line1', 'city', 'state', 'country')
    list_filter = ('is_default',)