from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer



class ShippingAdressSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(many=False)
    class Meta:
        model = ShippingAdress
        fields=['id','buyer','name','mobile','pincode','locality','city','state','landmark']

        def validate(self, attrs):
            print(attrs)
  
