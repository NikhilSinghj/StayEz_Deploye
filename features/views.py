from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, PropertyDetails
from .serializers import CartSerializer
from properties.serializers import PropertyCardListSerializer

class AddToCartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        ppty_id = request.data.get('id')
        
        if Cart.objects.filter(ppty_id=ppty_id).exists():
            return Response({'detail': 'Property already in cart'}, status=status.HTTP_400_BAD_REQUEST)
        
        ppty = PropertyDetails.objects.get(id=ppty_id)
        Cart.objects.create(ppty=ppty)
        return Response({'success':'Added to Cart'}, status=status.HTTP_201_CREATED)

class RemoveFromCartView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def delete(self, request, id, *args, **kwargs):
        try:
            cart_item = Cart.objects.get(ppty=id)
            cart_item.delete()
            return Response({'msg':'Deleted'},status=status.HTTP_204_NO_CONTENT)

        except Cart.DoesNotExist:
            return Response({'error': 'Property not found in cart'}, status=status.HTTP_400_BAD_REQUEST)
        

class UserCartView(generics.ListAPIView):
    serializer_class = PropertyCardListSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.filter()  # filter by current user
        property_ids = cart.values_list('ppty_id', flat=True)  # extract IDs in a single query
        return PropertyDetails.objects.filter(id__in=property_ids)  # filter by property IDs


class CheckCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter()  