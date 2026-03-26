from django.contrib import admin
from .models import Categories, Products, ProductImage, ProductVariant

@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category_id', 'brand', 'is_active', 'is_digital', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'alt_text', 'is_thumbnail', 'created_at')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'sku', 'price', 'stock_quantity', 'created_at')
