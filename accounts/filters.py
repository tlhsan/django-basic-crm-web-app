import django_filters
from .models import *

# creating an order filter class for searching
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer']
