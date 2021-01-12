from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name = 'customer')
        instance.groups.add(group) 
        # to assign the new user as a customer
        Customer.objects.create(
            user = instance,
            name = instance.username
            )
        print("Profile was created using signals")

post_save.connect(customer_profile, sender = User)