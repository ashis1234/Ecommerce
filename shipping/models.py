from django.db import models
from user.models import User
from order.models import Order

class ShippingAdress(models.Model):
	buyer = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	mobile = models.CharField(max_length=20)
	pincode = models.IntegerField()
	locality = models.CharField(max_length=30)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	landmark = models.CharField(max_length=50)


	def __str__(self):
		return self.name

class Transaction(models.Model):
	buyer = models.ForeignKey(User,on_delete=models.CASCADE)
	address = models.ForeignKey(ShippingAdress,on_delete=models.CASCADE)
	order = models.ForeignKey(Order,on_delete=models.CASCADE)
	paymentID = models.CharField(max_length=100, null=True,blank=True)
	paymentToken = models.CharField(max_length=100, null=True,blank=True)

	def __str__(self):
		return str(self.transcaction_hash)