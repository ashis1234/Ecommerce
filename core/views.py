from .models import Customer, Order, OrderItem, Product, ShippingAddress
from django.shortcuts import render
from django.shortcuts import render
from django.core.exceptions import MultipleObjectsReturned
from django.http import JsonResponse
import json
import datetime
# Create your views here.

def store(request):
    products = Product.objects.all()
    order = {'get_total_price' : 0,'get_total_quantity' : 0,'shipping' : False}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        for i in cart:
            order['get_total_quantity'] += cart[i]['quantity']
    return render(request,'core\store.html',{'order' : order,'products': products})
# guest user


def cart(request):
    order = {'get_total_price' : 0,'get_total_quantity' : 0,'shipping' : False}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        # {'1': {'quantity': 2}, '2': {'quantity': 3}, '3': {'quantity': 1}, '4': {'quantity': 1}, '5': {'quantity': 1}}
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        for i in cart:
            product = Product.objects.get(id=i)
            order['get_total_quantity'] += cart[i]['quantity']
            order['get_total_price'] += product.price*cart[i]['quantity']
            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total' : product.price*cart[i]['quantity'],
            }
            items.append(item)
    context= {'items': items,'order' : order}
    return render(request, 'core/cart.html', context)


def checkout(request):
    order = {'get_total_price' : 0,'get_total_quantity' : 0,'shipping' : False}
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        for i in cart:
            product = Product.objects.get(id=i)
            order['get_total_quantity'] += cart[i]['quantity']
            order['get_total_price'] += product.price*cart[i]['quantity']
            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total' : product.price*cart[i]['quantity'],
            }
            items.append(item)        
    context= {'items': items,'order' : order}
    return render(request,'core\checkout.html',context)




def updateItem(request):
    data = json.loads(request.body)
    product_id = data['productid']
    action = data['action']
    print(product_id,action)
    customer = request.user.customer
    product = Product.objects.get(id = product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem,created = OrderItem.objects.get_or_create(order=order,product = product)
    if action == 'add':
        orderitem.quantity = orderitem.quantity+1
    else:
        orderitem.quantity = orderitem.quantity-1
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()
    
    return JsonResponse(data,safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(request.body)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        print("login first")
        name = data['form']['name']
        email = data['form']['email']
        items = []
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        customer,created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()
        order = Order.objects.create(
            customer = customer,
            complete = False,
        )

        for i in cart:
            product = Product.objects.get(id=i)
            item = OrderItem.objects.create(
                product=product,
                order = order,
                quantity = cart[i]['quantity'],
            )
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_total_price):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shippinginfo']['address'],
            city = data['shippinginfo']['city'],
            state = data['shippinginfo']['state'],
            zipcode = data['shippinginfo']['zipcode'],
            
        )
    return JsonResponse('payment succesfull',safe=False)