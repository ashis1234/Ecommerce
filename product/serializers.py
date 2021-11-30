from json.decoder import JSONDecodeError
import re
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from user.serializers import UserSerializer
import json

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields=['id','cat_name']
        extra_kwargs ={
            'cat_name': {
                'validators': [UniqueValidator(queryset=Category.objects.all())]
            }
        }

  

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



class ProductSerializer(serializers.ModelSerializer):
    tags = CategorySerializer(
        many=True,
        source='tag_set'
    )
    seller = UserSerializer(many=False)

    class Meta:
        model = Product
        fields = ('id', 'title','price','tags','seller','digital','image','description','created_at')
    