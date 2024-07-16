from django.urls import path
from .views import (
    PropertyDetailsCreateView, PropertyDetailsListView, PropertyDetailsListView,
    PropertyDetailsUpdateView, PropertyDetailsDeleteView,
    RoomDetailsCreateView, #RoomDetailsListView, RoomDetailsDetailView,
    # RoomDetailsUpdateView, RoomDetailsDeleteView,
    # AnemitiesCreateView, AnemitiesListView, AnemitiesDetailView,
    # AnemitiesUpdateView, AnemitiesDeleteView,
    ImagesCreateView, ImagesListView,
    ImagesUpdateView, ImagesDeleteView,PropertyCardView
)


urlpatterns = [
    # PropertyDetails URLs
    # path('filters/', FilterOptionsView.as_view(), name='filter-options'),
    path('property/', PropertyDetailsCreateView.as_view(), name='property-create'),
    path('property/list/', PropertyCardView.as_view(), name='property-list'),
    path('property/list/<int:pk>/', PropertyDetailsListView.as_view(), name='property-detail'),
    path('property/update/<int:pk>/', PropertyDetailsUpdateView.as_view(), name='property-update'),
    path('property/delete/<int:pk>/', PropertyDetailsDeleteView.as_view(), name='property-delete'),

    # RoomDetails URLs
    path('room/', RoomDetailsCreateView.as_view(), name='room-create'),
    # path('room/list/', RoomDetailsListView.as_view(), name='room-list'),
    # path('room/<int:pk>/', RoomDetailsDetailView.as_view(), name='room-detail'),
    # path('room/update/<int:pk>/', RoomDetailsUpdateView.as_view(), name='room-update'),
    # path('room/delete/<int:pk>/', RoomDetailsDeleteView.as_view(), name='room-delete'),

    # Anemities URLs
    # path('anemities/', AnemitiesCreateView.as_view(), name='anemities-create'),
    # path('anemities/list/', AnemitiesListView.as_view(), name='anemities-list'),
    # path('anemities/<int:pk>/', AnemitiesDetailView.as_view(), name='anemities-detail'),
    # path('anemities/update/<int:pk>/', AnemitiesUpdateView.as_view(), name='anemities-update'),
    # path('anemities/delete/<int:pk>/', AnemitiesDeleteView.as_view(), name='anemities-delete'),

    # Images URLs
    path('images/', ImagesCreateView.as_view(), name='images-create'),
    path('images/<int:pk>/', ImagesListView.as_view(), name='images-list'),
    path('images/update/<int:pk>/', ImagesUpdateView.as_view(), name='images-update'),
    path('images/delete/<int:pk>/', ImagesDeleteView.as_view(), name='images-delete'),
    path('all/<int:id>/images/', ImagesListView.as_view(), name='room-images-list'),

    # path('rooms/', RoomListView.as_view(), name='room-list'),

    path('listfilters/', PropertyCardView.as_view()),
]






