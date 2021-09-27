from django.urls import path
from . import views
from allauth.account.views import LoginView, SignupView 

urlpatterns = [
    path('', views.empty),
    path('home/', views.home, name='home'),
    path('menu/', views.Menu, name='menu'),
    path('cart/', views.CartView, name='cart'),
    path('orders/', views.orderhistory, name='orders'),
    path('ordersummary/', views.summary, name='ordersummary'),
    path('ordersuccess/', views.success, name='ordersuccess'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', SignupView.as_view(), name='register'),
    path('profile/', views.ProfileView, name='profile'),
    path('namechange/', views.NameChange, name='namechange'),
    path('addresschange/', views.AddressChange, name='addresschange'),
    path('addressremove/', views.AddressRemove, name='addressremove'),
    path('addressadd/', views.AddressAdd, name='addressadd'),
    path('accountsetup/', views.SetUp, name='setup'),
    path('admindashboard/', views.adminDashboard, name='admindashboard'),
    path('admindashboardorders/', views.adminDashboardorders, name='admindashboardorders'),
    path('mailtest/', views.mail),
]
