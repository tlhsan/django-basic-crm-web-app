from django.shortcuts import render, redirect
from .models import *
from .forms import CreateUserForm,OrderForm, CustomerForm
# to allow multiple create fields 
from django.forms import inlineformset_factory
# allow search fields
from .filters import OrderFilter
# getting django's built in user form
from django.contrib.auth.forms import UserCreationForm
# for getting the flash messages
from django.contrib import messages
# for login autheticate and logout
from django.contrib.auth import login,authenticate,logout
# for now use this way, on big project use middleware
from django.contrib.auth.decorators import login_required
# for custom decorators 
from .decorators import authenticated_user_decorator, admin_only_decorator, restrict_role_decorator
# to access the auth group model
from django.contrib.auth.models import Group

# Create your views here.

# View for registration
@authenticated_user_decorator
def registerPageView(request):
    # usually this is done using middleware but at the moment lets do it manually

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
        # all the user registration stuffs are done on signals now    
            # get the group to be assigned
            # group = Group.objects.get(name = 'customer')
            # user.groups.add(group) 
            # # to assign the new user as a customer
            # Customer.objects.create(
            #     user = user
            # )
            # get the username
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for '+ username)
            return redirect('accounts:login')

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

# View for login
@authenticated_user_decorator
def loginPageView(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, 'Username or Password Incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)

# View for logout
def logOutView(request):
    logout(request)
    return redirect('accounts:login')

# View for login
def userPageView(request):
    orders = request.user.customer.order_set.all()
    #for the stats. orders count - total, pending, delivered
    order_total_count = orders.count()
    order_pending_count = orders.filter(status='Pending').count()
    order_delivered_count = orders.filter(status='Delivered').count()
    context = {
        'orders': orders,
        'order_total_count': order_total_count,
        'order_pending_count': order_pending_count,
        'order_delivered_count': order_delivered_count,
    }
    return render(request, 'accounts/user.html', context)

# user settings page
@login_required(login_url='accounts:login')
@restrict_role_decorator(allowed_roles=['customer'])
def accountSettingsPage(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {
        'form': form
    }
    return render(request, 'accounts/account_settings.html', context)

# View for home
@login_required(login_url='accounts:login')
@admin_only_decorator
@restrict_role_decorator(allowed_roles=['admin'])
def home(request):
    # getting all the model objects
    orders = Order.objects.all()
    customers = Customer.objects.all()
    products = Product.objects.all()
    customers_count = customers.count()

    #for the stats. orders count - total, pending, delivered
    order_total_count = orders.count()
    order_pending_count = orders.filter(status='Pending').count()
    order_delivered_count = orders.filter(status='Delivered').count()

    context = {
        'customers':customers,
        'products':products,
        'orders':orders,
        'order_total_count':order_total_count,
        'order_pending_count':order_pending_count,
        'order_delivered_count':order_delivered_count,
        }
    return render(request, 'accounts/dashboard.html', context)

# View for product
@login_required(login_url='accounts:login')
def products(request):
    #getting all the product objects from the DB
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})

# View for customer
@login_required(login_url='accounts:login')
def customer(request, pk):
    #getting specific customer object from the DB
    customer = Customer.objects.get(id = pk)
    # getting the child class stuff, format - var objectsRelatedToChild = parentClass.ChildClass_set.all()
    customer_all_orders = customer.order_set.all()
    order_count = customer_all_orders.count()
    # getting the filter 
    myorderFilter = OrderFilter(request.GET, queryset=customer_all_orders)
    customer_all_orders = myorderFilter.qs
    context = {
        'customer': customer,
        'customer_all_orders':customer_all_orders,
        'order_count':order_count,
        'myorderFilter': myorderFilter,
    }
    return render(request, 'accounts/customer.html', context)

# View for order create
@login_required(login_url='accounts:login')
def orderCreate(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3)
    #get specific customer
    customer = Customer.objects.get(id = pk)
    # importing the form for order creation note: initial sets the specific variable
    #form = forms.OrderForm(initial={'customer': customer})
    # pass a set of form instead 
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        #form = forms.OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset,
    }
    return render(request, 'accounts/order_form.html', context)

# View for order update
@login_required(login_url='accounts:login')
def orderUpdate(request, pk):
    # get the specific order data
    order = Order.objects.get(id = pk)
    form = forms.OrderForm(instance = order)

    if request.method == 'POST':
        form = forms.OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'accounts/order_form.html', context)

# View for customer create
@login_required(login_url='accounts:login')
def customerCreate(request):
    form = forms.CustomerForm()

    if request.method == 'POST':
        form = forms.CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/customer_form.html', context)

# View for customer update
@login_required(login_url='accounts:login')
def customerUpdate(request, pk):
    #get specific customer
    customer = Customer.objects.get(id = pk)
    form = forms.CustomerForm(instance = customer)

    if request.method == 'POST':
        form = forms.CustomerForm(request.POST, instance = customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'accounts/customer_form.html', context)

# View for customer delete
def customerDelete(request, pk):
    customer = Customer.objects.get(id = pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')
    context = {
        'item': customer,
    }
    return render(request, 'accounts/delete_page.html', context)

# View for order delete
def orderDelete(request, pk):
    order = Order.objects.get(id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item': order,
    }
    return render(request, 'accounts/delete_page.html', context)