from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .filters import ProductFilter
from .forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

def register(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error has occured!')

    context={'form':form}
    return render(request,'store/register.html',context)


def loginUser(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    # else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,"Credential Invalid")

        return render(request,'store/login.html')

class home(View):
    def get (self,request):
        products=Product.objects.all()
        topwear=Product.objects.filter(Category='TW')
        bottomwear=Product.objects.filter(Category='BW')
        context={'topwear':topwear,'bottomwear':bottomwear,'products':products}
        return render(request,'store/index.html',context)

class ProuctDetailView(View):
    def get(self,request,pk):

        allproducts=Product.objects.all()
        product=Product.objects.get(id=pk)
        already_in_cart=False
        if request.user.is_authenticated:
            already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        

        context={'product':product,'allproducts':allproducts,'already_in_cart':already_in_cart}
        return render(request,'store/detail.html',context)

def searchbar(request):
    q=request.GET.get('product')if request.GET.get('product')!=None else ''
    products=Product.objects.filter(Q(title__icontains=q) 
    |Q(description__icontains=q)
    |Q(brand__icontains=q)
    |Q(Category__icontains=q))
    context={'items':products}
    return render (request,'store/shop.html',context)






def searchproduct(request,data):
    items=Product.objects.filter(brand=data)
    # if items.exists():
    #     print('hi')
    # else:
    #     print("ëmpty")
    if request.method=='GET':
        filterset=ProductFilter(request.GET,queryset=items)
        items=filterset.qs

    context={'items':items,'filterset':filterset}
    return render (request,'store/shop.html',context)

@login_required(login_url='login')

def addtocart (request):
    user=request.user
    prodid=request.GET.get('prodid')
    product=Product.objects.get(id=prodid)
    cart=Cart.objects.create(user=user,product=product)
    cart.save()
    return redirect('cart')

@login_required(login_url='login')
def showcart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    # print(cart)
    amount=0.0
    shipping=100.0
    tempamnt=0.0
    totalamnt=0.0
    cart_prod=[p for p in Cart.objects.all() if p.user==user]
    if cart_prod :
        for prod in cart_prod:
            tempamnt=prod.quantity*prod.product.discounted_price
            amount+=tempamnt
        totalamnt=shipping+amount
        context={'carts':cart,'totalamnt':totalamnt,'amount':amount}
        return render(request,'store/cart.html',context)
    else:
        return render(request,'store/emptycart.html')


@login_required(login_url='login')
def plus_cart(request):
    if request.method=='GET':
        prodid=request.GET['prod_id']
        prodoper=request.GET['prod_oper']
        print(prodid)
        print(prodoper)
        cart=Cart.objects.get(Q(user=request.user)&Q(product=prodid))
        if prodoper=='add':
            cart.quantity+=1
        else:
            cart.quantity-=1

        
        cart.save()
        amount=0.0
        shipping=100
        cart_product=[p for p in Cart.objects.all()if p.user==request.user]
        for p in cart_product:
            tempamnt=p.quantity*p.product.discounted_price
            amount+=tempamnt
        totalamnt=shipping+amount
        data={
            'amount':amount,
            'quantity':cart.quantity,
            'totalamnt':totalamnt,
        }
        return JsonResponse(data)


@login_required(login_url='login')
def remove_cart(request):
    if request.method=='GET':
        prodid=request.GET['prod_id']
       
        print(prodid)
        
        cart=Cart.objects.get(Q(user=request.user)&Q(product=prodid))
        cart.delete()
        amount=0.0
        shipping=100
        cart_product=[p for p in Cart.objects.all()if p.user==request.user]
        for p in cart_product:
            tempamnt=p.quantity*p.product.discounted_price
            amount+=tempamnt
        totalamnt=shipping+amount
        data={
            'amount':amount,
            
            'totalamnt':totalamnt,
        }
        return JsonResponse(data)


@login_required(login_url='login')
def ShippingAddress(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    # print(cart)
    amount=0.0
    shipping=100.0
    tempamnt=0.0
    totalamnt=0.0
    cart_prod=[p for p in Cart.objects.all() if p.user==user]
    if cart_prod :
        for prod in cart_prod:
            tempamnt=prod.quantity*prod.product.discounted_price
            amount+=tempamnt
        totalamnt=shipping+amount
        if request.method=="POST":
            name=request.POST.get('name')
            locality=request.POST.get('locality')
            city=request.POST.get('city')
            state=request.POST.get('state')
            zipcode=request.POST.get('zipcode')
            method=request.POST.get('payment')

            customer= Customer.objects.create(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode,payement_method=method)
            customer.save()
            cust_method=customer.payement_method
           
            cust_id=customer.id
            
            customer=Customer.objects.get(id=cust_id)
            for c in cart:
                order=OrderPlaced.objects.create(user=request.user,customer=customer,product=c.product,quantity=c.quantity)
                order.save()
                c.delete()
                request.session['od_id']=order.id
                request.session['od_amnt']=totalamnt
                if cust_method=="Khalti":
                    return redirect('khaltirequest')
          
        
    context={'carts':cart,'totalamnt':totalamnt,'amount':amount}

    return render(request,'store/shipping_detail.html',context)



class KhaltirequestView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        od_amnt=request.session['od_amnt']
        od_id=request.session['od_id']
        order=OrderPlaced.objects.get(id=od_id)
        
        context={
            "ttlamnt":od_amnt,
            'order':order
              
        }
    
        return render(request,'store/khaltirequest.html',context)


class KhaltiVerifyView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        token=request.GET.get("token")
        amount=request.GET.get("amount")
        od_id=request.GET.get('order_id')
        order_obj=OrderPlaced.objects.get(id=od_id)
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount
         }
        headers = {
            # use secret key here of yours
          "Authorization": "Key ....."
         }

        response = requests.post(url, payload, headers = headers)
        response_obj=response.json()
        print(response_obj)
        if response_obj.get("idx"):
            success=True
            order_obj.payment_completed=True
            order_obj.save()
        else:
            success=False    
        data={"success":success}
        return JsonResponse(data)


@login_required(login_url='login')
def orders(request):
    user=request.user
    orders=OrderPlaced.objects.filter(user=user)
    return render(request,'store/orders.html',{'orders':orders})


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

