from django.db.models.fields import DateField
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, CustomerForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models.functions import Cast
from django.db import connection
from django.db.models import Sum,F
from .models import *
from . import Functions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.gis.geos import Point
import random

from django.db.models import F
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

'''
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
'''

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
                lattitude = float(request.POST.get('lat'))
                longitude = float(request.POST.get('lng'))
                pnt = Point(longitude,lattitude)
                obj.Address = pnt
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
        x = Customer.objects.filter(user=request.user)
        if len(x) != 1:
            return redirect(reverse('setup'))
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
    AllMenuItems = Products.objects.all()
    context = {}
    if request.user.is_authenticated:
        x = Customer.objects.filter(user=request.user)
        if len(x) != 1:
            return redirect(reverse('setup'))
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['AllCartItems'] = cartitems
        context['Cartobjects'] = queryset
    else:
        context['AllCartItems'] = None
    if request.user.is_authenticated:
        x = Customer.objects.filter(user=request.user)
        if len(x) != 1:
            return redirect(reverse('setup'))
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context['AllCartItems'] = cartitems
        context['Cartobjects'] = queryset
    else:
        context['AllCartItems'] = None
    if request.method == 'GET':
        ProductID = request.GET.get('ProductID')
        Update = request.GET.get("Update")
        if Update is not None:
            if Update == "add":
                currentCustomer = Customer.objects.get(user=request.user)
                addedproduct = Products.objects.get(ProductID = int(ProductID))
                Cart.objects.filter(CustomerID=currentCustomer, ProductID = addedproduct).update(Quantity=F('Quantity') + 1)
                print("adone")
            elif Update == "subtract":
                currentCustomer = Customer.objects.get(user=request.user)
                addedproduct = Products.objects.get(ProductID = int(ProductID))
                Cart.objects.filter(CustomerID=currentCustomer, ProductID = addedproduct).update(Quantity=F('Quantity') - 1)
                print("done")
            elif Update == "remove":
                currentCustomer = Customer.objects.get(user=request.user)
                addedproduct = Products.objects.get(ProductID = int(ProductID))
                instance = Cart.objects.filter(CustomerID=currentCustomer, ProductID = addedproduct)
                if len(instance) > 0:
                    instance = instance[0]
                else:
                    instance = Cart.objects.get(CustomerID=currentCustomer, ProductID = addedproduct)
                instance.delete()
        elif ProductID is not None:
            currentCustomer = Customer.objects.get(user=request.user)
            addedproduct = Products.objects.get(ProductID = int(ProductID))
            cartitem = Cart(CustomerID= currentCustomer, ProductID= addedproduct)
            cartitem.save(force_insert=True)
        else:
            page = request.GET.get('page', 1)
            paginator = Paginator(AllMenuItems, 8)
            try:
                Items = paginator.page(page)
            except PageNotAnInteger:
                Items = paginator.page(1)
            except EmptyPage:
                Items = paginator.page(paginator.num_pages)
            context['AllMenuItems'] = Items


    return render(request, 'baseapp/menu.html', context)


def CartView(request):
    if request.user.is_authenticated:
        x = Customer.objects.filter(user=request.user)
        if len(x) != 1:
            return redirect(reverse('setup'))
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context = {'cartitems':cartitems}
        context['Cartqueryset'] = queryset
        if request.method == 'GET':
            ProductID = request.GET.get('ProductID')
            Update = request.GET.get("Update")
            if Update is not None:
                if Update == "add":
                    currentCustomer = Customer.objects.get(user=request.user)
                    addedproduct = Products.objects.get(ProductID = int(ProductID))
                    Cart.objects.filter(CustomerID=currentCustomer, ProductID = addedproduct).update(Quantity=F('Quantity') + 1)
                    print("adone")
                elif Update == "subtract":
                    currentCustomer = Customer.objects.get(user=request.user)
                    addedproduct = Products.objects.get(ProductID = int(ProductID))
                    Cart.objects.filter(CustomerID=currentCustomer, ProductID = addedproduct).update(Quantity=F('Quantity') - 1)
                    print("done")
                elif Update == "remove":
                    currentCustomer = Customer.objects.get(user=request.user)
                    addedproduct = Products.objects.get(ProductID = int(ProductID))
                    instance = Cart.objects.filter(CustomerID=currentCustomer, ProductID = addedproduct)
                    if len(instance) > 0:
                        instance = instance[0]
                    else:
                        instance = Cart.objects.get(CustomerID=currentCustomer, ProductID = addedproduct)
                    instance.delete()
            elif ProductID is not None:
                currentCustomer = Customer.objects.get(user=request.user)
                addedproduct = Products.objects.get(ProductID = int(ProductID))
                cartitem = Cart(CustomerID= currentCustomer, ProductID= addedproduct)
                cartitem.save(force_insert=True)
        return render(request, 'baseapp/cart.html', context)
    
    return redirect(reverse('login'))

def summary(request):
    if request.user.is_authenticated:
        x = Customer.objects.filter(user=request.user)
        if len(x) != 1:
            return redirect(reverse('setup'))
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems,itemswithqty = [],[]
        for obj in queryset:
            cartitems.append(obj.ProductID)
            itemswithqty.append((obj.ProductID, obj.Quantity))
        context = {'objects':cartitems}
        context["itemswithqty"] = itemswithqty
        totalcost = 0
        for productpair in itemswithqty:
            totalcost += productpair[0].Price * productpair[1]
        context['totalcost'] = totalcost
        context['cust'] = currentCustomer

        if request.method == 'POST':
            uid = request.POST.get('csrfmiddlewaretoken')
            for product in itemswithqty:
                newOrder = Orders(
                    OrderNumber = uid,
                    CustomerID = currentCustomer,
                    ProductID = product[0],
                    OrderStatus = 'Order Success',
                    ItemPrice = product[0].Price,
                    Qty = product[1],
                )
                newOrder.save(force_insert=True)
                instance = Cart.objects.get(CustomerID=currentCustomer, ProductID = product[0])
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
        #print(currentCustomer.Address)
        return render(request, 'baseapp/success.html', context)
    else:
        return redirect(reverse('login'))


def orderhistory(request):
    if request.user.is_authenticated:
        x = Customer.objects.filter(user=request.user)
        if len(x) != 1:
            return redirect(reverse('setup'))
        currentCustomer = Customer.objects.get(user=request.user)
        queryset = Cart.objects.filter(CustomerID=currentCustomer)
        cartitems = []
        for obj in queryset:
            cartitems.append(obj.ProductID)
        context = {'cartitems':cartitems}
        AllOrderedObjects = Orders.objects.filter(CustomerID= currentCustomer).order_by('OrderNumber')
        #print(AllOrderedObjects)
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
        if len(o) > 0:
            SeparateOrders.append(o)
        if SeparateOrders == []:
            SeparateOrders.append(o)
        SeparateOrders.sort(reverse=True, key= lambda x: x[0].DateOrdered)
        OrderCosts = Functions.PriceList(SeparateOrders)
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
                print(requiredOrder)
                context['total'] = total
                context['backurl'] = 'orders'
                return render(request, 'baseapp/orderview.html', context)

        return render(request, 'baseapp/orders.html', context)
    else:
        return redirect(reverse('login'))

def ProfileView(request):
    if request.user.is_authenticated:
        x = Customer.objects.filter(user=request.user)
        if len(x) != 1:
            return redirect(reverse('setup'))
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
            return render(request, 'baseapp/profile.html', context)
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


def mail(request):
    if request.user.is_authenticated:
        form = CustomerForm()
        context = {'form':form}

        if request.method == 'POST':
            print(request.POST)
            return render(request, 'baseapp/test.html', context)

        return render(request, 'baseapp/test.html', context)
    else:
        return redirect(reverse('home'))
    


def adminDashboard(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            context = {}
            currentCustomer = Customer.objects.get(user=request.user)
            queryset = Cart.objects.filter(CustomerID=currentCustomer)
            cartitems = []
            for obj in queryset:
                cartitems.append(obj.ProductID)
            context['cartitems'] = cartitems
            context['customer'] = currentCustomer

            
            #CUSTOMERS:
            customerresultset = Customer.objects.all()
            print(len(customerresultset))
            allcustomers = []
            count = 0
            for cust in customerresultset:
                if count == 0:
                    tempset = []
                if count == 9:
                    count = 0
                    tempset.append(cust)    
                    allcustomers.append(tempset)
                    continue

                tempset.append(cust)
                count+=1
            if len(tempset) > 0:
                allcustomers.append(tempset)

            context['allcustomers'] = allcustomers
            #END OF CUSTOMER TABLE



            #ORDERS TABLE
            context['totalorders'] = len(Orders.objects.all())
            

            #PRODUCT QUANTITIES
            quantities = Orders.objects.values("ProductID").order_by("ProductID").annotate(quantity=Sum('Qty'))
            maxprod = [0,0]
            salesdist = {'Burgers':0, 'Pizzas':0, 'Wraps':0, 'Sides':0}
            total_revenue = 0
            for item in quantities:
                if item['quantity'] >= maxprod[1]:
                    maxprod[0] = item['ProductID']
                    maxprod[1] = item['quantity']
                if item['ProductID'] <= 10:
                    salesdist['Burgers'] += item['quantity']
                elif 11 <= item['ProductID'] <= 17:    
                    salesdist['Pizzas'] += item['quantity']
                elif 24 <= item['ProductID'] <= 26:    
                    salesdist['Wraps'] += item['quantity']
                else:
                    salesdist['Sides'] += item['quantity']
                total_revenue += Products.objects.get(ProductID=item['ProductID']).Price * item['quantity']
            maxprod[0] = Products.objects.get(ProductID=maxprod[0])

            cursor = connection.cursor()
            cursor.execute('SELECT  "CustomerID_id", SUM("ItemPrice" * "Qty") FROM PUBLIC.BASEAPP_ORDERS GROUP BY "CustomerID_id" ORDER BY SUM("ItemPrice" * "Qty") DESC LIMIT 1;')
            row = cursor.fetchall()
            
            context['maxcust'] = [Customer.objects.get(id=int(row[0][0])).CustomerName, int(row[0][1])]
            context['maxproduct'] = maxprod
            context['revenue'] = total_revenue
            newdist = []
            newdist.append(salesdist['Wraps'])
            newdist.append(salesdist['Pizzas'])
            newdist.append(salesdist['Sides'])
            newdist.append(salesdist['Burgers'])
            finaldist = ''
            for i in newdist:
                finaldist += str(i) + ','
            context['salesdist'] = finaldist


            cursor = connection.cursor()
            cursor.execute('SELECT DATE_PART(\'week\', DATE("DateOrdered")) AS Week, SUM("ItemPrice"*"Qty") FROM PUBLIC.BASEAPP_ORDERS GROUP BY DATE_PART(\'week\', DATE("DateOrdered"));')
            row = cursor.fetchall()
            weeklabels,weekvalues = [],[]
            for i in row:
                weeklabels.append('Week ' + str(int(i[0])))
                weekvalues.append(int(i[1]))
            context['weeklabels'] = weeklabels
            context['weekvalues'] = weekvalues
            return render(request, 'baseapp/adminDashboard.html', context)
        else:
            messages.info(request, 'You are not authorised to view this page')
            return(redirect(reverse('home')))
    else:
        return redirect(reverse('login'))

def adminDashboardorders(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            context = {}
            currentCustomer = Customer.objects.get(user=request.user)
            queryset = Cart.objects.filter(CustomerID=currentCustomer)
            cartitems = []
            for obj in queryset:
                cartitems.append(obj.ProductID)
            context['cartitems'] = cartitems
            context['customer'] = currentCustomer
            
            AllOrderedObjects = Orders.objects.all().order_by('OrderNumber')
        #print(AllOrderedObjects)
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
            if len(o) > 0:
                SeparateOrders.append(o)
            if SeparateOrders == []:
                SeparateOrders.append(o)
            SeparateOrders.sort(reverse=True, key= lambda x: x[0].DateOrdered)
            OrderCosts = Functions.PriceList(SeparateOrders)
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
                    #print(requiredOrder)
                    context['total'] = total
                    context['backurl'] = 'admindashboard'
                    return render(request, 'baseapp/orderview.html', context)

            return render(request, 'baseapp/adminDashboardorders.html', context)
        else:
            messages.info(request, 'You are not authorised to view this page')
            return(redirect(reverse('home')))
    else:
        return redirect(reverse('login'))