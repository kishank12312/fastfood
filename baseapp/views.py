from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from .models import *
# Create your views here.


def RegisterView(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == "POST":

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
            login(request,new_user)
            return redirect(reverse('setup'))

    context = {'form': form}
    return render(request, 'baseapp/register.html', context)

def LoginView(request):
    context = {}
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('Username'),password=request.POST.get('Password'))
        
        if user is not None:
            login(request, user)
            if request.GET.get('next') == '/menu/':
                return redirect(reverse('menu'))
            else:
                return redirect(reverse('home'))
        else:
            messages.info(request, 'Username or Password is incorrect.')

    return render(request, 'baseapp/login.html', context)

def LogoutView(request):
    logout(request)
    return redirect(reverse('login'))

def SetUp(request):
    if request.user.is_authenticated:
        form = CustomerForm()
        context = {'form':form}

        if request.method == 'POST':
            #print(request.POST)
            form = CustomerForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.user = request.user
                obj.save()
            return redirect(reverse('home'))

        return render(request, 'baseapp/accountsetup.html', context)
    else:
        return redirect(reverse('home'))

def empty(request):
    return redirect('home/')

def home(request):
    context = {}
    if request.user.is_authenticated:
        currentCustomer = Customer.objects.get(user=request.user)
        context['u'] = currentCustomer
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['AllCartItems'] = cartitems
        return render(request, 'baseapp/index.html', context)


    return render(request, 'baseapp/index.html')


def Menu(request):
    burgers = Products.objects.filter(Category='Burger')
    burgergrouped,burgerset = [],[]
    for burger in burgers:
        if len(burgerset) < 4:
            burgerset.append(burger)
        if len(burgerset) == 4:
            burgergrouped.append(burgerset)
            burgerset = []
    if len(burgerset) > 0:
        burgergrouped.append(burgerset)
    pizzas = Products.objects.filter(Category='Pizza')
    pizzagrouped,pizzaset = [],[]
    for pizza in pizzas:
        if len(pizzaset) < 4:
            pizzaset.append(pizza)
        if len(pizzaset) == 4:
            pizzagrouped.append(pizzaset)
            pizzaset = []
    if len(pizzaset) > 0:
        pizzagrouped.append(pizzaset)
    wraps = Products.objects.filter(Category='Wraps')
    wrapgrouped,wrapset = [],[]
    for wrap in wraps:
        if len(wrapset) < 4:
            wrapset.append(wrap)
        if len(wrapset) == 4:
            wrapgrouped.append(wrapset)
            wrapset = []
    if len(wrapset) > 0:
        wrapgrouped.append(wrapset)
    sides = Products.objects.filter(Category='Sides')
    sidegrouped,sideset = [],[]
    for side in sides:
        if len(sideset) < 4:
            sideset.append(side)
        if len(sideset) == 4:
            sidegrouped.append(sideset)
            sideset = []
    if len(sideset) > 0:
        sidegrouped.append(sideset)
    context = {'burgergrouped':burgergrouped, 'pizzagrouped':pizzagrouped, 'wrapgrouped': wrapgrouped, 'sidegrouped':sidegrouped}
    if request.user.is_authenticated:
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['AllCartItems'] = cartitems
    else:
        context['AllCartItems'] = None
    if request.method == 'GET':
        ProductID = request.GET.get('ProductID')
        if ProductID is not None:
            currentCustomer = Customer.objects.get(user=request.user)
            addedproduct = Products.objects.get(ProductID = int(ProductID))
            cartitem = Cart(CustomerID= currentCustomer, ProductID= addedproduct)
            cartitem.save(force_insert=True)


    return render(request, 'baseapp/menu.html', context)


def CartView(request):
    if request.user.is_authenticated:
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context = {'cartitems':cartitems}
        if request.method == "GET":
            if request.GET.get('ProductID') is not None:
                ProductID = request.GET.get('ProductID')
                product = Products.objects.get(ProductID = int(ProductID))
                instance = Cart.objects.get(CustomerID=currentCustomer, ProductID = product)
                instance.delete()
        return render(request, 'baseapp/cart.html', context)
    
    return redirect(reverse('login'))

def summary(request):
    if request.user.is_authenticated:
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context = {'objects':cartitems}
        totalcost = 0
        for product in cartitems:
            totalcost += product.Price
        context['totalcost'] = totalcost
        context['cust'] = currentCustomer


        if request.method == 'POST':
            uid = request.POST.get('csrfmiddlewaretoken')
            address = request.POST.get('Address')
            for product in cartitems:
                newOrder = Orders(
                    OrderNumber = uid,
                    CustomerID = currentCustomer,
                    ProductID = product,
                    Address = address,
                    OrderStatus = 'Order Success',
                    ItemPrice = product.Price,
                )
                newOrder.save(force_insert=True)
                instance = Cart.objects.get(CustomerID=currentCustomer, ProductID = product)
                instance.delete()
            return redirect(reverse('ordersuccess'))

        return render(request, 'baseapp/summary.html', context)
    
    return redirect(reverse('login'))

def success(request):
    if request.user.is_authenticated:
        context = {}
        currentCustomer = Customer.objects.get(user=request.user)
        context['u'] = currentCustomer
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['AllCartItems'] = cartitems
        return render(request, 'baseapp/success.html', context)
    else:
        return redirect(reverse('login'))


def orderhistory(request):
    if request.user.is_authenticated:
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context = {'cartitems':cartitems}
        AllOrderedObjects = Orders.objects.filter(CustomerID= currentCustomer).order_by('OrderNumber')
        if len(AllOrderedObjects) == 0:
            context['SeparateOrders'] = [] 
            context['OrderCosts'] = []
            return render(request, 'baseapp/orders.html', context)
        SeparateOrders = []
        TempOrderNum = AllOrderedObjects[0].OrderNumber
        o = []
        for Object in AllOrderedObjects:
            if Object.OrderNumber == TempOrderNum:
                o.append(Object)
            else:
                SeparateOrders.append(o)
                o = []
                o.append(Object)
                TempOrderNum = Object.OrderNumber
        if SeparateOrders == []:
            SeparateOrders.append(o)
        OrderCosts = []
        for OrderSet in SeparateOrders:
            TempCost = 0
            for IndividualOrder in OrderSet:
                TempCost += IndividualOrder.ItemPrice
            OrderCosts.append(TempCost)
        context['SeparateOrders'] = SeparateOrders 
        context['OrderCosts'] = OrderCosts
        if request.method == "GET":
            if request.GET.get('OrderView') is not None:
                onum = request.GET.get('OrderView')
                requiredOrder = None
                index = 0
                for Order in SeparateOrders:
                    if Order[0].OrderNumber == onum:
                        requiredOrder = Order
                        total = OrderCosts[index]
                    index+=1
                context = {}
                context['Order'] = requiredOrder
                context['total'] = total
                return render(request, 'baseapp/orderview.html', context)

        return render(request, 'baseapp/orders.html', context)
    else:
        return redirect(reverse('login'))

def ProfileView(request):
    if request.user.is_authenticated:
        context = {}
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['cartitems'] = cartitems
        context['customer'] = currentCustomer
        AllOrderedObjects = Orders.objects.filter(CustomerID= currentCustomer).order_by('OrderNumber')
        if len(AllOrderedObjects) == 0:
            context['SeparateOrders'] = [] 
            context['OrderCosts'] = []
            return render(request, 'baseapp/orders.html', context)
        SeparateOrders = []
        TempOrderNum = AllOrderedObjects[0].OrderNumber
        o = []
        for Object in AllOrderedObjects:
            if Object.OrderNumber == TempOrderNum:
                o.append(Object)
            else:
                SeparateOrders.append(o)
                o = []
                o.append(Object)
                TempOrderNum = Object.OrderNumber
        if SeparateOrders == []:
            SeparateOrders.append(o)
        context['separateorders'] = SeparateOrders
        return render(request, 'baseapp/profile.html', context)
    else:
        return redirect(reverse('login'))

def NameChange(request):
    if request.user.is_authenticated:
        context = {}
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['cartitems'] = cartitems
        context['customer'] = currentCustomer
        if request.method == 'POST':
            new = request.POST.get('NewName')
            currentCustomer.CustomerName = new
            currentCustomer.save(force_update=True)
            return redirect(reverse('profile'))
        return render(request, 'baseapp/namechange.html', context)
    else:
        return redirect(reverse('login'))
def AddressRemove(request):
    if request.user.is_authenticated:
        context = {}
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['cartitems'] = cartitems
        context['customer'] = currentCustomer
        currentCustomer.Address = ""
        currentCustomer.save(force_update=True)
        return render(request, 'baseapp/addressremove.html', context)
    else:
        return redirect(reverse('login'))
def AddressAdd(request):
    if request.user.is_authenticated:
        context = {}
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['cartitems'] = cartitems
        context['customer'] = currentCustomer
        if request.method == 'POST':
            new = request.POST.get('NewAddress')
            currentCustomer.Address = new
            currentCustomer.save(force_update=True)
            return redirect(reverse('profile'))
        return render(request, 'baseapp/addAdress.html', context)
    else:
        return redirect(reverse('login'))
def AddressChange(request):
    if request.user.is_authenticated:
        context = {}
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['cartitems'] = cartitems
        context['customer'] = currentCustomer
        if request.method == 'POST':
            new = request.POST.get('NewAddress')
            currentCustomer.Address = new
            currentCustomer.save(force_update=True)
            return redirect(reverse('profile'))
        return render(request, 'baseapp/addresschange.html', context)

    else:
        return redirect(reverse('login'))
