from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics  
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import generics,views,permissions
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from django.http.response import JsonResponse
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser,IsStaffUser
from django.contrib.auth import authenticate, login, logout
from .models import User,Dropdown,OwnerDetails
from properties.models import PropertyDetails
from .serializers import (UserRegistrationSerializer,OwnerRegistrationSerializer,LoginSerializer,PasswordResetRequestSerializer,
                           PasswordResetSerializer,UserSerializer,PasswordChangeSerializer
                          )



from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'csrfToken': get_token (request)})


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        print(request.data)
        user = User.objects.filter(email = request.data.get('email'))
        if user:
            return Response({'message': 'Email already exist'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User Registered Succesfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OwnerRegistrationView(APIView):
    def post(self, request):
        serializer = OwnerRegistrationSerializer(data=request.data)
        print(request.data)
        user = User.objects.filter(email = request.data.get('email'))
        if user:
            return Response({'message': 'Email already exist'}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Owner Registered Succesfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        print(request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            password = serializer.validated_data['password']
            
            # Fetch the user using username or email
            try:
                user = User.objects.get(Q(contact=user) | Q(email=user))
            except User.DoesNotExist:
                user = None
            
            # If user is found, use the username to authenticate
            if user:
                user = authenticate(request, contact=user.contact, password=password)
                if user:
                    login(request, user)
                    return Response({"message": "User logged in successfully."}, status=status.HTTP_200_OK)
            
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     authentication_classes = [CsrfExemptSessionAuthentication,SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         logout(request)
#         return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
    


        

class PasswordResetRequestView(views.APIView):
    authentication_classes = [CsrfExemptSessionAuthentication,SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            contact_or_email = serializer.validated_data.get('contact') or serializer.validated_data.get('email')
            user = User.objects.filter(Q(contact=contact_or_email) | Q(email=contact_or_email)).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"https://127.0.0.1:8000/resetpass/{uid}/{token}/"
                send_mail(
                    'Password Reset Request',
                    f'Use the link to reset your password: {reset_url}',
                    'nikhilsinghj80@gmail.com',
                    [user.email]
                )
                return Response({'message': 'Password reset link has been sent to your email'}, status=status.HTTP_200_OK)
            return Response({'message': 'Wrong Email'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetView(views.APIView):
    authentication_classes = [CsrfExemptSessionAuthentication,SessionAuthentication, BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, uid, token):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')

            try:
                id = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=id)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid token or user ID'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password"]}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileAPIView(generics.ListAPIView):
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id).values()



def property_dropdown(request):
    ppty_type = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Type of Property')).values('id', 'name'))
    amenity = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Amenities')).values('id', 'name'))
    avl_for = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Avialable For')).values('id', 'name'))
    near_college = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Nearest Educational Institute')).values('id', 'name'))
    pay_duration = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Rent Pay Duration')).values('id', 'name'))
    mess_facility = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Mess Facility')).values('id', 'name'))
    security_features = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Securtiy features')).values('id', 'name'))
    lifestyle = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Lifestyle')).values('id', 'name'))
    rules = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Rules')).values('id', 'name'))


    data = {
            "ppty_type":ppty_type,
            "amenity":amenity,  
            "avl_for":avl_for,
            "near_college":near_college,
            "pay_duration":pay_duration,
            "mess_facility":mess_facility,
            "security_features":security_features,
            "lifestyle":lifestyle,
            "rules":rules

        }
    
    return JsonResponse(data)

def room_dropdown(request):
    property = list(PropertyDetails.objects.filter(deleted_status=False,owner=request.user.id).values('id', 'property_name'))
    # amenity = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Amenities')).values('id', 'name'))
    seater = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Seats Per Room')).values('id', 'name'))
    furnishing = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Lifestyle')).values('id', 'name'))
    kitchen = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Kitchen')).values('id', 'name'))
    washroom = list(Dropdown.objects.filter(deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Washroom')).values('id', 'name'))

    data = {
            "property":property,
            "seater":seater,  
            "furnishing":furnishing,
            "kitchen":kitchen,
            "washroom":washroom,

        }
    
    test = Dropdown.objects.get(deleted_status=False,name='Type of Property')
    print(test.id)

    return JsonResponse(data)



def filter_set(request):
    property_type = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Type of Property')).values('id', 'name'))
    amenity = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Amenities')).values('id', 'name'))
    avl_for = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Avialable For')).values('id', 'name'))
    near_college = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Nearest Educational Institute')).values('id', 'name'))
    pay_duration = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Rent Pay Duration')).values('id', 'name'))
    mess_facility = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Mess Facility')).values('id', 'name'))
    seater = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Seats Per Room')).values('id', 'name'))
    furnishing = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Lifestyle')).values('id', 'name'))
    kitchen = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Kitchen')).values('id', 'name'))
    washroom = list(Dropdown.objects.filter(filter=1,deleted_status=False,relation=Dropdown.objects.get(deleted_status=False,name='Washroom')).values('id', 'name'))

    data = {
            "property_type":property_type,
            "amenity":amenity,  
            "avl_for":avl_for,
            "near_college":near_college,
            "pay_duration":pay_duration,
            "mess_facility":mess_facility,
            "seater":seater,
            "furnishing":furnishing,
            "kitchen":kitchen,
            "washroom":washroom

        }
    
    
    return JsonResponse(data)

    

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


from .serializers import CustomTokenObtainSerializer, LogoutSerializer

class LogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication,SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)




        # 3f691196734aaa40c352b3cf820d6419