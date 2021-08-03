from django.urls import path
from . import views

urlpatterns = [
    path('', views.empty),
    path('home/', views.home, name='home'),
    path('menu/', views.Menu, name='menu'),
    path('cart/', views.CartView, name='cart'),
    path('orders/', views.orderhistory, name='orders'),
    path('ordersummary/', views.summary, name='ordersummary'),
    path('ordersuccess/', views.success, name='ordersuccess'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.RegisterView, name='register'),
    path('profile/', views.ProfileView, name='profile'),
    path('namechange/', views.NameChange, name='namechange'),
    path('addresschange/', views.AddressChange, name='addresschange'),
    path('addressremove/', views.AddressRemove, name='addressremove'),
    path('addressadd/', views.AddressAdd, name='addressadd'),
    path('accountsetup/', views.SetUp, name='setup'),
]
