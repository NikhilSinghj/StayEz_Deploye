import json
from django.db import transaction
from rest_framework import generics,status
from .filters import PropertyFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from main.authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.views import APIView 
from .models import PropertyDetails, RoomDetails, Amenities, Images,Dropdown
from .serializers import PropertyDetailsSerializer, ImagesSerializer,PropertyListSerializer, RoomDetailListSerializer,RoomDetailsSerializer,PropertyCardListSerializer

# PropertyDetails Views
class PropertyDetailsCreateView(APIView):
    def post(self, request):
        # Extract the JSON data from 'newData'
        new_data = request.data.get('newData')
        if new_data:
            new_data = json.loads(new_data)
            
        # Extract the image file
        cover_image = request.FILES.get('cover_image')

        print(cover_image)
        
        # Combine parsed JSON data with the cover_image file
        if cover_image:
            new_data['cover_image'] = cover_image
        
        # Pass the combined data to the serializer
        serializer = PropertyDetailsSerializer(data=new_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PropertyCardView(generics.ListAPIView):
    authentication_classes = [CsrfExemptSessionAuthentication,SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = PropertyCardListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter

    def get_queryset(self):
        queryset = PropertyDetails.objects.filter(deleted_status=False)
        
        return queryset

class PropertyDetailsListView(generics.RetrieveAPIView):
    serializer_class = PropertyListSerializer

    def get_queryset(self):
        queryset = PropertyDetails.objects.filter(deleted_status=False)

        return queryset

# class PropertyDetailsUpdateView(generics.UpdateAPIView):
#     queryset = PropertyDetails.objects.all()
#     serializer_class = PropertyDetailsSerializer

#     def perform_update(self, serializer):
#         instance = self.get_object()
#         validated_data = serializer.validated_data

#         # Define the fields that are allowed to be updated
#         allowed_fields = {'property_name', 'phone_no', 'starting_price', 'description'}

#         # Update only the allowed fields
#         for attr, value in validated_data.items():
#             if attr in allowed_fields:
#                 setattr(instance, attr, value)
        
#         instance.save()
#         return Response({"message": "Property details updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)


# class PropertyDetailsListView(generics.ListAPIView):
#     queryset = PropertyDetails.objects.all()
#     serializer_class = PropertyDetailsSerializer


class PropertyDetailsUpdateView(generics.UpdateAPIView):
    queryset = PropertyDetails.objects.all()
    serializer_class = PropertyDetailsSerializer

class PropertyDetailsDeleteView(generics.DestroyAPIView):
    queryset = PropertyDetails.objects.all()
    serializer_class = PropertyDetailsSerializer

# RoomDetails Views

class RoomDetailsCreateView(generics.CreateAPIView):
    serializer_class = RoomDetailsSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        # Fetch the existing PropertyDetails instance
        try:
            property_details = PropertyDetails.objects.get(id=1)  # Change this to get the actual property ID
        except PropertyDetails.DoesNotExist:
            return Response({"error": "Property not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch Dropdown instances
        try:
            seater = Dropdown.objects.get(id=data.get('seater'))
            furnished = Dropdown.objects.get(id=data.get('furnished'))
            kitchen = Dropdown.objects.get(id=data.get('kitchen'))
            washroom = Dropdown.objects.get(id=data.get('washroom'))
        except Dropdown.DoesNotExist:
            return Response({"error": "Invalid dropdown ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare room details data
        room_details_data = {
            'ppty': property_details,
            'seater': seater,
            'total_rooms': data.get('total_rooms'),
            'occupied_rooms': data.get('occupied_rooms'),
            'price': data.get('price'),
            'furnished': furnished,
            'kitchen': kitchen,
            'washroom': washroom,
        }

        # Handle amenities data
        amenities_data = request.data.getlist('amenities.amnty')
        amenities_list = [{'amnty': Dropdown.objects.get(id=amenity_id)} for amenity_id in amenities_data]

        # Handle images data
        images_data = request.FILES.getlist('images.image')

        # Use a transaction to ensure atomicity
        with transaction.atomic():
            room_details = RoomDetails.objects.create(**room_details_data)

            try:
                # Create room amenities
                for amenity_data in amenities_list:
                    Amenities.objects.create(room=room_details, ppty=property_details, **amenity_data)

                # Create room images
                for image_data in images_data:
                    Images.objects.create(room=room_details, images=image_data)

            except Exception as e:
                # Rollback the transaction if any error occurs
                raise ValidationError({"error": f"Failed to create room amenities or images: {str(e)}"})

        return Response({"message": "Room details created successfully"}, status=status.HTTP_201_CREATED)


# class RoomDetailsListView(generics.ListAPIView):
#     queryset = RoomDetails.objects.all()
#     serializer_class = RoomDetailsSerializer

# class RoomDetailsDetailView(generics.RetrieveAPIView):
#     queryset = RoomDetails.objects.all()
#     serializer_class = RoomDetailsSerializer

# class RoomDetailsUpdateView(generics.UpdateAPIView):
#     queryset = RoomDetails.objects.all()
#     serializer_class = RoomDetailsSerializer

# class RoomDetailsDeleteView(generics.DestroyAPIView):
#     queryset = RoomDetails.objects.all()
#     serializer_class = RoomDetailsSerializer

# Anemities Views
# class AnemitiesCreateView(generics.CreateAPIView):
#     queryset = Anemities.objects.all()
#     serializer_class = AnemitiesSerializer

# class AnemitiesListView(generics.ListAPIView):
#     queryset = Anemities.objects.all()
#     serializer_class = AnemitiesSerializer

# class AnemitiesDetailView(generics.RetrieveAPIView):
#     queryset = Anemities.objects.all()
#     serializer_class = AnemitiesSerializer

# class AnemitiesUpdateView(generics.UpdateAPIView):
#     queryset = Anemities.objects.all()
#     serializer_class = AnemitiesSerializer

# class AnemitiesDeleteView(generics.DestroyAPIView):
#     queryset = Anemities.objects.all()
#     serializer_class = AnemitiesSerializer

# Images Views
class ImagesCreateView(generics.CreateAPIView):
    serializer_class = ImagesSerializer
    permission_classes=[IsAuthenticated]

    def get(self):
        return Images.objects.filter(pk=self.request.user.id,deleted_status=False).values()

class ImagesListView(generics.RetrieveAPIView):
    serializer_class = ImagesSerializer
    # permission_classes=[IsAuthenticated]

    def get_queryset(self):
        id = self.kwargs['id']
        room_id = RoomDetails.objects.get()
        return Images.objects.filter(room_id=room_id)

class ImagesUpdateView(generics.UpdateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class ImagesDeleteView(generics.DestroyAPIView):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer







