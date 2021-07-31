from django.urls import path
from . import views

urlpatterns = [
    path('', views.empty),
    path('home/', views.home, name='home'),
    path('menu/', views.Menu, name='menu'),
    path('cart/', views.CartView, name='cart'),
    path('ordersummary/', views.summary, name='ordersummary'),
    path('ordersuccess/', views.success, name='ordersuccess'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.RegisterView, name='register'),
    path('accountsetup/', views.SetUp, name='setup'),
]
