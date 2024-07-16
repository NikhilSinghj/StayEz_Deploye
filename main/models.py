from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, contact, password=None, **extra_fields):
        if not contact:
            raise ValueError('The Contact field must be set')
        extra_fields.pop('username', None)

        # extra_fields.setdefault('username', contact)  # Bypass the username requirement
        user = self.model(contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(contact, password, **extra_fields)


class User(AbstractUser): 
    username = None
    contact = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'contact'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return str(self.pk)
    

class BaseModel(models.Model):
    created_time=models.DateTimeField(auto_now_add=True)
    deleted_time = models.DateTimeField(null=True)
    deleted_status=models.BooleanField(default=False)
    class Meta:
        abstract = True

class Dropdown(BaseModel):
    name = models.CharField(max_length=50)
    relation = models.ForeignKey("Dropdown", on_delete=models.SET_NULL, null=True)
    order_by = models.PositiveIntegerField(default=0)
    filter=models.BooleanField(default=0)


class OwnerDetails(BaseModel):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,related_name='user_idt')
    o_contact = models.CharField(max_length=10)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.PositiveIntegerField()
    country = models.CharField(max_length=50,default="India")
    id_proof_type = models.ForeignKey(Dropdown,on_delete=models.SET_NULL,null=True,related_name='id_proof')
    proof_image = models.ImageField(upload_to='id_proof')
