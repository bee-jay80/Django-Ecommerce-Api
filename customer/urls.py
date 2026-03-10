from django.urls import path
from .views import CustomerRegisterView, LoginView, LogoutView, CustomerProfileView

urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='customer-login'),
    path('logout/', LogoutView.as_view(), name='customer-logout'),
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    # path('logout/', LogoutView.as_view(), name='customer-logout'),
    # path('profile/', ProfileView.as_view(), name='customer-profile'),
    # path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    # path('addresses/<uuid:pk>/', AddressDetailView.as_view(), name='address-detail'),
]