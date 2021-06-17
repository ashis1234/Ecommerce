from django.urls import path,include
from .views import *

urlpatterns = [
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('update_item/',updateItem,name='update_item'),
    path('process_order/',processOrder,name='process_order'),
    path('',store,name='store'),
]

