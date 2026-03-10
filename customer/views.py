from .models import Customer, Addresses, CustomerProfile
from .serializers import CustomerSerializer, CustomerRegisterSerializer, AddressSerializer, LoginSerializer, CustomerProfileSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .utils.emails import send_welcome_email

from rest_framework.parsers import MultiPartParser, FormParser


class CustomerRegisterView(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerRegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # No authentication needed for registration

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()

        # Create a CustomerProfile for the new customer
        CustomerProfile.objects.create(customer=customer)

        # Send welcome email
        send_welcome_email(customer)

        response =  Response({
            "message": "Customer registered successfully",
            "customer": CustomerSerializer(customer).data,
        }, status=status.HTTP_201_CREATED)

        return response

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # No authentication needed for login

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            customer = Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not customer.check_password(password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(customer)
        access_token = str(refresh.access_token)

        response =  Response({
            "message": "Login successful",
            "customer": CustomerSerializer(customer).data
        }, status=status.HTTP_200_OK)

        # Set HttpOnly cookie with access token
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True,  # Set to True in production
            samesite='Lax'
        )

        response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,  # Set to True in production
            samesite='Lax'
        )
        return response


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        try:
            return self.request.user.profile
        except CustomerProfile.DoesNotExist:
            CustomerProfile.objects.create(customer=self.request.user)
            return self.request.user.profile

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)