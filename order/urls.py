from django.urls import path
from .views import TransactionView,OrderView,AddToCart,Increase_quantity,Decrease_quantity,RemoveItem,CartView,getTotalquantity

urlpatterns = [
    path('order/',OrderView.as_view(),name="order"),
    path('addtocart/',AddToCart.as_view(),name="addtocart"),
    path('increment/<int:id>/',Increase_quantity.as_view(),name='increment'),
    path('decrement/<int:id>/',Decrease_quantity.as_view(),name='decrement'),
    path('remove/<int:id>/',RemoveItem.as_view(),name='remove'),
    path('cartview/<str:username>/',CartView.as_view(),name="cartview"),
    path('getTotalQuantity/<str:username>/',getTotalquantity.as_view(),name='getTotalQuantity'),
    path('transaction/',TransactionView.as_view(),name='transaction')
]
