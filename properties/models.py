from django.db import models
from main.models import BaseModel,OwnerDetails,Dropdown


class PropertyDetails(BaseModel):
    owner=models.ForeignKey(OwnerDetails,on_delete=models.SET_NULL,null=True,related_name='owner_idty')
    # property_id = models.CharField(max_length=30,unique=True)
    property_name = models.CharField(max_length=50)
    property_type = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='ppty_type')
    phone_no=models.CharField(max_length=15)
    avl_for = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='avl_type')
    starting_price = models.FloatField()
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.PositiveIntegerField()  # lat and long
    country = models.CharField(max_length=50,default="India")
    deleted_status=models.BooleanField(default=False)
    near_college = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='near_clg')
    dist_from_college = models.FloatField(default=50.00)
    security_charges = models.FloatField(default=0.00)
    rnt_pay_duration = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='rnt_pay')
    # add_charges = models.JSONField(default=dict) /
    security_features = models.JSONField(default=dict)
    # bill_included = models.JSONField(default=dict)
    lifestyle = models.JSONField(default=dict)
    mess_facility = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='mess_fclty') 
    rules = models.JSONField(default=dict)
    description = models.TextField(max_length=500, default=None)
    cover_image = models.ImageField(upload_to='cover_image')




class RoomDetails(BaseModel):
    ppty = models.ForeignKey(PropertyDetails,on_delete=models.SET_NULL,null=True,related_name='ppty_detail')
    seater = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='seater_inf')
    total_rooms = models.PositiveSmallIntegerField()
    occupied_rooms = models.PositiveSmallIntegerField() 
    price = models.FloatField()  
    furnished = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='fur_inf')
    kitchen = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='kit_rel')
    washroom = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='wash_rel')


class Amenities(models.Model):
    amnty=models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='amnt_idty')
    ppty = models.ForeignKey(PropertyDetails,on_delete=models.SET_NULL,null=True,related_name='ppty_amnt')
    room = models.ForeignKey(RoomDetails,on_delete=models.SET_NULL,null=True,related_name='rm_amnt')


class Images(BaseModel):
    room = models.ForeignKey(RoomDetails,on_delete=models.SET_NULL,null=True,related_name='room_img')
    images = models.ImageField(upload_to='room_images')

class RoomSharing(BaseModel):
    room = models.ForeignKey(RoomDetails,on_delete=models.SET_NULL,null=True,related_name='room_detail')
    room_no = models.PositiveSmallIntegerField()
    sharing_with = models.JSONField(default=dict)

    


