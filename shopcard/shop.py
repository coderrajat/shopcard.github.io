from django.http import HttpResponse
from django.shortcuts import render
from .models import product, contact, checkout, updateorder
from math import ceil
import json
import smtplib
from django.views.decorators.csrf import csrf_exempt
from paytmchecksum import PaytmChecksum

M_key='u2gKfnU&pSFT@Z1H'
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

def research(word,item):
    if word in item.product_name.lower() or word in item.desc.lower() or word in item.category.lower():
        return True
    else:
        return False

def Search(request):
    word=request.GET.get('search')
    prodlist = []
    catprod = product.objects.values('category', 'id')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prodtem = product.objects.filter(category=cat)
        prod=[item for item in prodtem if research(word,item)]
        n = len(prod)
        nslide = ceil(n / 4)

        if len(prod) != 0:
            prodlist.append([prod, range(1, nslide), nslide])

    param = {'prodlist': prodlist,'msg':''}
    if len(prodlist)==0 or len(word)<4:
        param = {'msg':'Ops product not found'}

    return render(request,'search.html',param)

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
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'tracker.html')


def Productview(request,myid):
    produc=product.objects.filter(id=myid)
    price=product.objects.filter(id=myid).values('price')
    print(produc[0],price[0].get('price'))
    return render(request,'prodview.html',{"produc":produc[0],"price":price[0].get('price'),'myid':myid})

def Checkout(request):
    if(request.method=='POST'):
        prod_json = request.POST.get('itemjson', '')
        amount = request.POST.get("amount",'')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address-1','')+' '+request.POST.get('address-2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zipcode', '')
        prod_order = checkout(amount=amount,item_json=prod_json,name=name,email=email,phone=phone,address=address,city=city,state=state,zip_code=zip_code)
        prod_order.save()
        print(amount, email,prod_order.prod_id)
        update = updateorder(order_id=prod_order.prod_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = prod_order.prod_id
        param_dict = {
            'MID': "XLamRs07712538728009",
            'ORDER_ID': str(id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': str(email),
            'INDUSTRY_TYPE_ID': "Retail",
            'WEBSITE': "WEBSTAGING",
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/Handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = PaytmChecksum.generateSignature(param_dict, M_key)
        return render(request, 'pytm.html', {'param_dict': param_dict,'email':email})
        return render(request, 'checkout.html', {'thank': thank, 'id': id})
    return render(request,'checkout.html')



@csrf_exempt
def Handlerequest(request):
    #paytm will send request here
    form=request.POST
    checkout.objects.filter(prod_id=212).values('email')[0]['email']
    response_dict={}

    for i in form.keys():
        response_dict[i]=form[i]
        if i=='ORDERID':
            email = checkout.objects.filter(prod_id=form[i]).values('email')[0]['email']
            print(email)
        if i=='CHECKSUMHASH':
            checksum=form[i]
            print(checksum)
            varify=PaytmChecksum.verifySignature(response_dict,M_key,checksum)
            if varify:
                if response_dict['RESPCODE']=='01':
                    print('success')
                    print(email)
                    mes = f"From:{'shopcard'} \n\n Subject:{'Your order Payment successfuly'}"
                    server = smtplib.SMTP(host="smtp.gmail.com", port=587)
                    server.ehlo()
                    server.starttls()
                    server.ehlo()
                    try:
                        server.login("tomarrajat916@gmail.com", "rajathero1998")
                        try:
                            server.sendmail("tomarrajat916@gmail.com",email,mes)
                            print('successfully send')
                        except Exception as e:
                            print(e)
                        server.close()
                    except Exception as e:
                        print(e)
                        print("your google less secure setting is not allowed")
                else:
                    print("Opps! your payment is not success"+response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})

def Login(request):
    return render(request,'login.html')
def SignUp(request):
    return render(request,'SignUp.html')

