from django.db import models
from user.models import User
from product.models import Product

# Create your models here.
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.IntegerField(default=0,null=True,blank=True)

    def __str__(self):
        return str(self.id)
        
    # @property
    # def shipping(self):
    #     for item in self.orderitem_set.all():
    #         if item.product.digital == False:
    #             return True
    #     return False
    @property
    def get_total_price(self):
        orderitem = self.orderitem_set.all()
        a = [item.get_total for item in orderitem]
        x = sum(a)
        return int(x)
        
    def get_total_quantity(self):
        orderitems = self.orderitem_set.all()
        a = [item.quantity for item in orderitems]
        return sum(a)

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        return self.product.price * self.quantity


