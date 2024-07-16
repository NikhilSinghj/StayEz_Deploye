from rest_framework import serializers
from .models import PropertyDetails, RoomDetails, Amenities, Images, Dropdown, OwnerDetails

#-------------------------------------Property Creation-----------------------------------------------#

class AnemitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = '__all__'

class PropertyDetailsSerializer(serializers.ModelSerializer):
    amenities = AnemitiesSerializer(many=True, required=True, write_only=True)

    class Meta:
        model = PropertyDetails
        fields = '__all__'

    def validate_amenities(self, value):
        seen = set()
        for amenity in value:
            amnty_id = amenity['amnty']
            if amnty_id in seen:
                raise serializers.ValidationError("Duplicate amenities are not allowed.")
            seen.add(amnty_id)
        return value

    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        property_details = None

        try:
            property_details = PropertyDetails.objects.create(**validated_data)
            
            for amenity_data in amenities_data:
                if Amenities.objects.filter(ppty=property_details, amnty=amenity_data['amnty']).exists():
                    raise serializers.ValidationError(f"Amenity {amenity_data['amnty']} already exists for this property.")
                Amenities.objects.create(ppty=property_details, **amenity_data)
        
        except Exception as e:
            if property_details:
                property_details.delete()
            raise serializers.ValidationError(f"error: {str(e)}")
        
        return property_details



#------------------------------------- Listing of property serializers ---------------------------------------------#

# Card Listing

class AnemitiesCardListSerializer(serializers.ModelSerializer):
    amenity_name = serializers.CharField(source='amnty.name', required=False)

    class Meta:
        model = Amenities
        fields = ['id', 'amenity_name']

class RoomCardListSerializer(serializers.ModelSerializer):
    seater = serializers.CharField(source='seater.name', required=False)
    furnished = serializers.CharField(source='furnished.name', required=False)
    kitchen = serializers.CharField(source='kitchen.name', required=False)
    washroom = serializers.CharField(source='washroom.name', required=False)

    class Meta:
        model = RoomDetails
        fields = ['id','seater','furnished','kitchen','washroom']

class PropertyCardListSerializer(serializers.ModelSerializer):
    room_detail = RoomCardListSerializer(many=True, source='ppty_detail')
    ppty_amenity = AnemitiesCardListSerializer(many=True, source='ppty_amnt')
    property_type = serializers.CharField(source='property_type.name', required=False)
    avl_for = serializers.CharField(source='avl_for.name', required=False)
    near_college = serializers.CharField(source='near_college.name', required=False)
    mess_facility = serializers.CharField(source='mess_facility.name', required=False)
    rnt_pay_duration = serializers.CharField(source='rnt_pay_duration.name', required=False)

    class Meta:
        model = PropertyDetails
        fields = ['id','property_name','avl_for','near_college','mess_facility',
                'rnt_pay_duration','property_type','starting_price','dist_from_college',
                'room_detail','ppty_amenity','cover_image']


#Detail Listing

class OwnerDetailListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    class Meta:
        model = OwnerDetails
        fields = ['first_name','last_name','o_contact']

class ImageDetailListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Images

        fields = ['id','images']

    def to_representation(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(instance.images.url)
        return instance.images.url

class AnemitiesDetailListSerializer(serializers.ModelSerializer):
    amenity_name = serializers.CharField(source='amnty.name', required=False)

    class Meta:
        model = Amenities
        fields = ['id', 'amenity_name']

class RoomDetailListSerializer(serializers.ModelSerializer):
    room_amnt = AnemitiesDetailListSerializer(many=True, required=False, source='rm_amnt')
    room_images = ImageDetailListSerializer(many=True,source='room_img',required=False)
    seater = serializers.CharField(source='seater.name', required=False)
    furnished = serializers.CharField(source='furnished.name', required=False)
    kitchen = serializers.CharField(source='kitchen.name', required=False)
    washroom = serializers.CharField(source='washroom.name', required=False)

    class Meta:
        model = RoomDetails
        exclude = ['created_time', 'deleted_time', 'deleted_status']

class PropertyListSerializer(serializers.ModelSerializer):
    owner = OwnerDetailListSerializer()
    room_detail = RoomDetailListSerializer(many=True, source='ppty_detail')
    ppty_amenity = AnemitiesDetailListSerializer(many=True, source='ppty_amnt')
    property_type = serializers.CharField(source='property_type.name', required=False)
    avl_for = serializers.CharField(source='avl_for.name', required=False)
    near_college = serializers.CharField(source='near_college.name', required=False)
    mess_facility = serializers.CharField(source='mess_facility.name', required=False)
    rnt_pay_duration = serializers.CharField(source='rnt_pay_duration.name', required=False)

    class Meta:
        model = PropertyDetails
        fields = ['id','property_type','avl_for','near_college','mess_facility','rnt_pay_duration','property_name',
                'phone_no','starting_price','address1','address2','city','state','zip_code','country',
                'dist_from_college','security_charges','security_features','lifestyle','rules','description',
                'owner','ppty_amenity','room_detail']
        # exclude = ['created_time', 'deleted_time', 'deleted_status']

#------------------------------------------ Room Details --------------------------------------------------------#

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id','room','images']

class RoomDetailsSerializer(serializers.ModelSerializer):
    room_amenities = AnemitiesSerializer(many=True, required=False)
    room_images = ImagesSerializer(many=True, required=False)

    class Meta:
        model = RoomDetails
        fields = ['id','seater','total_rooms','occupied_rooms','price','furnished','kitchen','washroom','room_amenities','room_images']




