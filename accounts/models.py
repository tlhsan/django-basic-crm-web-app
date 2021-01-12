from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Model Description : Customer model
class Customer(models.Model):
    # assigning a user to be a customer when registering 
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=20, null=True)
    profile_pic = models.ImageField(null = True)
    date_created = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return self.name

#Model Description : Tag model
class Tag(models.Model):
    name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name

#Model Description : Product model 
class Product(models.Model):
    #choices for category (set of tuples with keyValue)
    CATEGORY = (
        ('Sports', 'Sports'),
        ('Decor', 'Decor'),
        ('Food', 'Food')
    )
    name = models.CharField(max_length=250, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=250, null=True, choices=CATEGORY)
    details = models.TextField(blank=True)
    date_created = models.DateField(auto_now=True, null=True) 
    #Many to many relationship to allow having more than one reference
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

#Model Description : Product model 
class Order(models.Model):
    #choices for status (set of tuples with keyValue)
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )

    # link with the cus and pro models
    customer = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateField(auto_now=True, null=True)
    status = models.CharField(max_length=150, null=True, choices=STATUS)

    def __str__(self):
        return self.customer.name + ' - ' + self.product.name