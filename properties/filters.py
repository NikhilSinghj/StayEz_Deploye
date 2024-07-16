from django_filters import rest_framework as filters
from .models import PropertyDetails

class MultipleValuesCharFilter(filters.BaseCSVFilter, filters.CharFilter):
    pass

class PropertyFilter(filters.FilterSet):
    min_distance = filters.NumberFilter(field_name='dist_from_college', lookup_expr='gte') 
    max_distance = filters.NumberFilter(field_name='dist_from_college', lookup_expr='lte')
    min_price = filters.NumberFilter(field_name='starting_price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='starting_price', lookup_expr='lte')
    property_type = MultipleValuesCharFilter(field_name='property_type__name', lookup_expr='in')
    avl_for = MultipleValuesCharFilter(field_name='avl_for', lookup_expr='in')
    mess_facility = MultipleValuesCharFilter(field_name='mess_facility', lookup_expr='in')
    pay_duration = MultipleValuesCharFilter(field_name='rnt_pay_duration', lookup_expr='in')
    near_college = filters.CharFilter(field_name='near_college', lookup_expr='icontains')
    city = filters.CharFilter(lookup_expr='icontains')
    amenity = MultipleValuesCharFilter(field_name='ppty_amnt__amnty', lookup_expr='in')
    seater = MultipleValuesCharFilter(field_name='ppty_detail__seater', lookup_expr='in')
    furnishing = MultipleValuesCharFilter(field_name='ppty_detail__furnished', lookup_expr='in')
    kitchen = MultipleValuesCharFilter(field_name='ppty_detail__kitchen', lookup_expr='in')
    washroom = MultipleValuesCharFilter(field_name='ppty_detail__washroom', lookup_expr='in')
   
    # bill incuded  -- electricity
    # price -- room wise 
    class Meta:
        model = PropertyDetails
        fields = []
