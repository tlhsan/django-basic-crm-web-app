from django.forms import ModelForm
from .models import Order, Customer
# getting the django builtin user form
from django.contrib.auth.forms import UserCreationForm
# getting the django builtin user model to put in the usercreationform
from django.contrib.auth.models import User

# form class for order  
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
    # any specific form functions like filter and stuff will go here

# form class for customer  
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        # any specific form functions like filter and stuff will go here

# form class for custom UserCreationForm
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
