from django.db import models
from main.models import BaseModel,User
from properties.models import PropertyDetails

class RateReview(BaseModel):
    ppty = models.ForeignKey(PropertyDetails,on_delete=models.SET_NULL,null=True,related_name='ppty_ref')
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_ref')
    rating = models.FloatField(default=0.00)
    review = models.TextField(max_length=200)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='user_cart')
    ppty = models.ForeignKey(PropertyDetails,on_delete=models.SET_NULL,null=True,related_name='ppty_cart')
