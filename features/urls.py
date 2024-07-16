from django.urls import path
from .views import AddToCartView, RemoveFromCartView, UserCartView, CheckCartView

urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove/<int:id>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', UserCartView.as_view(), name='user-cart'),
    path('cart/check/', CheckCartView.as_view(), name='check-user-cart'),
]
