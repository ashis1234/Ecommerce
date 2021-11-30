from user.models import User
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import pagination
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics,status
from rest_framework.views import APIView
from user.serializers import UserSerializer


class ShippingAdressView(APIView):
	serializer_class = ShippingAdressSerializer
	def get(self, request, format=None):
		username = self.request.data.get('buyer')
		try:
			user_obj = User.objects.get(username = username)
		except:
			return Http404

		address = ShippingAdress.objects.filter(buyer=user_obj)
		serializer = self.serializer_class(address, many=True)
		return Response(serializer.data,status=status.HTTP_200_OK)

	def post(self,request,format=None):
		data = request.data
		try:
			username = data.get('buyer','')
			user_obj = User.objects.get(username=username)
		except:
			raise Http404
		name = data.get('name','')
		mobile = data.get('mobile','')
		pincode = data.get('pincode','')
		locality = data.get('locality','')
		city = data.get('city','')
		landmark = data.get('landmark','')
		state = data.get('state','')
		shipping_obj = ShippingAdress(buyer=user_obj,name=name,mobile=mobile,pincode=pincode,locality=locality,city=city,landmark=landmark,state=state)
		shipping_obj.save()
		serializer = self.serializer_class(shipping_obj)
		return Response(serializer.data,status=status.HTTP_201_CREATED)




class ShippingDetailView(APIView):
	serializer_class = ShippingAdressSerializer
	def get_object(self, pk):
		try:
			return ShippingAdress.objects.get(pk=pk)
		except ShippingAdress.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = self.serializer_class(snippet)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		snippet = self.get_object(pk)
		serializer = self.serializer_class(snippet, data=request.data)
		serializer.is_valid()
		validated_data = request.data

		if 'name' in validated_data:
			snippet.name = validated_data['name']
		if 'city' in validated_data:
			snippet.city = validated_data['city']
		if 'locality' in validated_data:
			snippet.locality = validated_data['locality']


		if 'state' in validated_data:
			snippet.state = validated_data['state']
		if 'landmark' in validated_data:
			snippet.landmark = validated_data['landmark']
		if 'mobile' in validated_data:
			snippet.mobile = validated_data['mobile']
		if 'pincode' in validated_data:
			snippet.pincode = validated_data['pincode']
		snippet.save()   
		serializer = self.serializer_class(snippet)
		return Response(serializer.data)

	def delete(self, request, pk, format=None):
		snippet = self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

