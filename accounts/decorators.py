from django.shortcuts import redirect
from django.http import HttpResponse

# custom decorators go here
def authenticated_user_decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
        #  here goes the additional instructions you want to run before it 
        #  executes the view_func from the views
        if request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# role-restricted(multiple groups) view decorator
# if you take a decorator parameter, then add another function 
# 'def decorator' to pass the view_func
def restrict_role_decorator(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # custom code goes here
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("you are not allowed to view")
        return wrapper_func
    return decorator

# admin only view decorator 
def admin_only_decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('accounts:user')
    return wrapper_func
