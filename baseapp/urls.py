from django.urls import path
from . import views

urlpatterns = [
    path('', views.empty),
    path('home/', views.home, name='home'),
    path('menu/', views.Menu, name='menu'),
    path('cart/', views.Menu, name='cart'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('register/', views.RegisterView, name='register'),
    path('accountsetup/', views.SetUp, name='setup'),
]
