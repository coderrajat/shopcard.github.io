from django.http import HttpResponse
from django.shortcuts import render
from .models import product, contact, checkout, updateorder
from math import ceil
import json

def home(request):
    '''prod=product.objects.all()
    n=len(prod)
    nslide=ceil(n/4)
    print(prod,"\n",n)
    prodlist=[[prod,range(1,nslide),nslide],[prod,range(1,nslide),nslide]]'''
    prodlist=[]
    catprod=product.objects.values('category','id')
    cats={item['category']for item in catprod}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n = len(prod)
        nslide = ceil(n / 4)
        prodlist.append([prod,range(1,nslide),nslide])
        param={'prodlist':prodlist}
    return render(request,'home.html',param)

def Contact(request):
    if request.method:
        name = request.POST.get('name','')
        phone = request.POST.get('phone','')
        email = request.POST.get('email','')
        desc = request.POST.get('desc','')
        Contac = contact(name=name, phone=phone, email=email, desc=desc)
        Contac.save()
    return render(request,'contact.html')

def About(request):
    return render(request,'about.html')
def Tracker(request):
    if request.method == "POST":
        order_id = request.POST.get("Order_id", '')
        email = request.POST.get('email', '')
        try:
            order = checkout.objects.filter(prod_id=order_id, email=email)
            if len(order) > 0:
                update = updateorder.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].item_json], default=str)
                print(order[0].item_json)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'tracker.html')


def Search(request):
    return render(request,'search.html')
def Productview(request,myid):
    produc=product.objects.filter(id=myid)
    return render(request,'prodview.html',{"produc":produc[0]})

def Checkout(request):
    if(request.method):
        prod_json = request.POST.get('itemjson', '')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address-1','')+' '+request.POST.get('address-2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zipcode', '')
        prod_order = checkout(item_json=prod_json,name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        prod_order.save()
        update = updateorder(order_id=prod_order.prod_id, update_desc="The order has been placed")
        update.save()
        id = prod_order.prod_id
    return render(request,'checkout.html',{'id':id})
