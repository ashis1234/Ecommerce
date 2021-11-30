from json.decoder import JSONDecodeError
import re
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from user.serializers import UserSerializer
import json
from product.serializers import ProductSerializer

class OrderItemSerializer1(serializers.ModelSerializer):
    product = ProductSerializer(
        many=False,
    )
    class Meta:
        model = OrderItem
        fields = ('id','product','quantity','date_added')
    

class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(many=False)
    orderitem_set = OrderItemSerializer1(read_only=True, many=True) # many=True is required
    class Meta:
        model = Order
        fields=['id','buyer','orderitem_set']

  


# class ProductListSerializer(serializers.ModelSerializer):
#     tags = CategorySerializer(
#         many=True,
#         read_only=True,
#         source='tag_set'
#     )
#     prices = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = ('id', 'title', 'tags', 'prices', 'image','created_at')

# Inherit from list serializer to get tags field.



class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(
        many=False,
        source='order'
    )
    product = ProductSerializer(
        many=False,
        source='product'
    )

    class Meta:
        model = OrderItem
        fields = ('id','product','order','quantity','date_added')
    