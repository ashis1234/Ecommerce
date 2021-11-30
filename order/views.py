import re
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import pagination
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from shipping.models import ShippingAdress,Transaction
import datetime
class OrderView(APIView):
    serializer_class = OrderSerializer    
    def get(self, request, format=None):
        products = Order.objects.all()
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class CartView(APIView):
    serializer_class = OrderSerializer
    def get(self,request,username = None):
        print("Fff")
        try:
            user_obj = User.objects.get(username=username)
        except:
            raise Http404
        try:
            order_obj = Order.objects.get(buyer=user_obj,complete=False)
        except:
            order_obj = Order.objects.create(buyer=user_obj)
        quantity = order_obj.get_total_quantity()
        price = order_obj.get_total_price
        serializer = self.serializer_class(order_obj)
        dict1 = dict(serializer.data)
        dict1['price'] = price
        dict1['quantity'] = quantity
        return Response(dict1,status=status.HTTP_200_OK)


class AddToCart(APIView):
    serializer_class = OrderSerializer
    def get_user(self,user):
        try:
            return User.objects.get(username=user)
        except:
            raise Http404

    def get_product(self,pname):
        try:
            return Product.objects.get(title=pname)
        except:
            raise Http404

    def post(self,request):
        validated_data = request.data
        username = validated_data.get('username','')
        quantity = validated_data.get('quantity',1)
        user_obj = self.get_user(username)
        if Order.objects.filter(buyer=user_obj,complete=False).exists():
            order_obj = Order.objects.get(buyer=user_obj,complete=False)
        else:
            order_obj = Order.objects.create(buyer=user_obj,complete=False)

        pname = validated_data.get('pname','')
        p_obj = self.get_product(pname)
        item = OrderItem.objects.get_or_create(order=order_obj,product=p_obj)[0]
        if "quantity" in validated_data:
            item.quantity = 0
        item.quantity += int(quantity)
        item.save()
        serializer = self.serializer_class(order_obj)
        dict1 = dict(serializer.data)
        dict1['quantity'] = order_obj.get_total_quantity()
        print(dict1['quantity'])
        return Response(dict1,status=status.HTTP_200_OK)

class getTotalquantity(APIView):
    def get(self,request,username=None):
        try:
            user_obj = User.objects.get(username=username)
        except:
            raise Http404
        try:
            order_obj = Order.objects.get(buyer=user_obj,complete=False)
        except:
            order_obj = Order.objects.create(buyer=user_obj)
        total = order_obj.get_total_quantity()
        return Response({"quantity" : total})


class Increase_quantity(APIView):
    def post(self,request,id=None):
        try:
            item = OrderItem.objects.get(id = id)
        except:
            raise Http404
        item.quantity+=1
        item.save()
        order_obj = item.order
        quantity = order_obj.get_total_quantity()
        return Response({"quantity":quantity,"message" : "Product Amount Successfully Incremented"},status=status.HTTP_200_OK)


class Decrease_quantity(APIView):
    def post(self,request,id=None):
        try:
            item = OrderItem.objects.get(id = id)
        except:
            raise Http404
        item.quantity-=1
        item.save()
        order_obj = item.order
        if item.quantity == 0:
            item.delete()
        quantity = order_obj.get_total_quantity()
        return Response({"quantity":quantity,"message" : "Product Amount Successfully Decremented "},status=status.HTTP_200_OK)

class RemoveItem(APIView):
    def delete(self,request,id):
        try:
            item = OrderItem.objects.get(id=id)
        except:
            raise Http404
        order_obj = item.order
        item.delete()
        quantity = order_obj.get_total_quantity()
        return Response({"quantity":quantity,"message" : "Product Amount Successfully Deleted "},status=status.HTTP_200_OK)

class TransactionView(APIView):
    def post(self,request):
        order_id = request.data.get('order_id',0)
        username = request.data.get('username',0)
        address_id = request.data.get('address_id',0)
        paymentID = request.data.get('paymentID','')
        paymentToken = request.data.get('paymentToken','')
        order = Order.objects.get(id = order_id)
        user = User.objects.get(username=username)
        address = ShippingAdress.objects.get(id=address_id)
        transaction_id = datetime.datetime.now().timestamp()
        transaction = Transaction.objects.create(paymentID=paymentID,paymentToken=paymentToken,buyer=user,order=order,address=address)
        transaction.save()
        order.complete = True
        order.save()
        return Response({'message':"Transacaion Succesfully Completed"},status=status.HTTP_200_OK)


