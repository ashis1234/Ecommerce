from django.urls import path
from .views import *


urlpatterns = [
	path('',ShippingAdressView.as_view(),name='shipping'),
	path('<int:pk>/',ShippingDetailView.as_view(),name='shipping-details'),
]