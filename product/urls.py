from django.urls import path
from .views import *
urlpatterns = [
    path('category/',CategoryView.as_view(),name='category'),
    path('category/<int:pk>/',CategoryDetailView.as_view(),name='category_detail'),
    path('product/',ProductView.as_view(),name='product'),
    path('product/<int:pk>/',ProductDetailView.as_view(),name='product_detail'),
    path('seller/<str:cName>',ProductBySeller.as_view(),name="productBySeller")
]

