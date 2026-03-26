from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from .models import Categories, Products, ProductImage, ProductVariant
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, ProductVariantSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
import logging


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Only create if the user is an admin
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can create categories.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can update categories.")

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Only create if the user is an admin
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can create products.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can update products.")
        
class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            # Log the error for debugging
            logger = logging.getLogger(__name__)
            logger.error(f"Image upload failed: {str(e)}")
            
            # Check if the error is related to network issues (e.g., Cloudinary upload failure)
            error_message = str(e).lower()
            if 'cloudinary' in error_message or 'maxretryerror' in error_message or 'nameresolutionerror' in error_message:
                return Response(
                    {"error": "Image upload failed due to network issues. Please check your internet connection and try again."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            else:
                # Re-raise other exceptions
                raise

    # Only create if the user is an admin
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can create product images.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can update product images.")
        
class ProductVariantListCreateView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Only create if the user is an admin
    def perform_create(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can create product variants.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only admins can update product variants.")

