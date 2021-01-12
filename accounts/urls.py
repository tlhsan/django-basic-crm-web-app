from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.registerPageView, name = 'register'),
    path('login/', views.loginPageView, name ='login'),
    path('logout/', views.logOutView, name ='logout'),
    path('customer/<str:pk>/', views.customer, name = 'customer'),
    path('products/', views.products, name = 'products'),
    path('ordercreate/<str:pk>/', views.orderCreate, name = 'ordercreate'),
    path('orderupdate/<str:pk>/', views.orderUpdate, name = 'orderupdate'),
    path('customercreate/', views.customerCreate, name = 'customercreate'),
    path('customerupdate/<str:pk>/', views.customerUpdate, name = 'customerupdate'),
    path('customerdelete/<str:pk>', views.customerDelete, name = 'customerdelete'),
    path('orderdelete/<str:pk>', views.orderDelete, name = 'orderdelete'),
    path('user/', views.userPageView, name = 'user'),
    path('accountsettings/', views.accountSettingsPage, name = 'account'),

    # django's forget password system with custom templates
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]

'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''