from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('product-images/', views.ProductImageListCreateView.as_view(), name='product-image-list-create'),
    path('product-variants/', views.ProductVariantListCreateView.as_view(), name='product-variant-list-create'),
]