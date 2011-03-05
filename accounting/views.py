# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from models import Manufacturer, Country, Type, Currency, Bicycle_Type, Bicycle,  Exchange,  FrameSize, Bicycle_Store, Bicycle_Sale
from forms import ContactForm, ManufacturerForm, CountryForm, CurencyForm, CategoryForm, BicycleTypeForm, BicycleForm, ExchangeForm, BicycleFrameSizeForm, BicycleStoreForm, BicycleSaleForm 


from models import Catalog, Client, ClientDebts, ClientCredits 
from forms import CatalogForm, ClientForm, ClientDebtsForm, ClientCreditsForm

from models import Dealer, DealerManager, DealerManager, DealerPayment, DealerInvoice, Bank
from forms import DealerManagerForm, DealerForm, DealerPaymentForm, DealerInvoiceForm, BankForm

from models import WorkGroup, WorkType, WorkShop, WorkStatus, WorkTicket, CostType, Costs
from forms import WorkGroupForm, WorkTypeForm, WorkShopForm, WorkStatusForm, WorkTicketForm, CostTypeForm, CostsForm
  
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


def search(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name__icontains=query)
        )
        results = Manufacturer.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("search.html", {
        "results": results,
        "query": query
    })


#def contact(request):
#    form = ContactForm()
#    return render_to_response('contact.html', {'form': form})


#def contact(request):
#    if request.method == 'POST':
#        form = ContactForm(request.POST)
#    else:
#        form = ContactForm()
#    return render_to_response('contact.html', {'form': form})


def del_logging(obj):
    file_name = 'test_log'
    log_path = settings.MEDIA_ROOT + 'logs/' + file_name + '.log'
    log_file = open(log_path, 'a')
    #for s in obj:
    #    result = result + ' | ' + s 
    #log_file.write("DELETE FROM TABLE " + table_name + " WHERE id = " + obj.name + "\n")
    log_file.write("DELETE FROM TABLE %s WHERE id = %s \n" % (obj._meta.verbose_name, obj.id) )
    #obj._meta.object_name
    #obj._meta.verbose_name
    #obj.__class__.__name__
    
    #for obj_f in obj._meta.get_all_field_names():
    #    log_file.write("Key %s Value \n" % obj_f)
        
    for f in obj._meta.fields:
        log_file.write("Key = " + f.name + " - ") # field name
        s = "Value = %s" % f.value_from_object(obj) + "\n"
        log_file.write(s.encode('cp1251'))
        #log_file.write("Value = %s" % f.value_from_object(obj).encode('cp1251') + "\n") # field value
            
    #log_file.write("DELETE FROM TABLE " + table_name + obj.name)
    log_file.close()


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('contact.html', {'form': form})

# ------------ Country -----------------

def country_add(request):
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Country(name=name).save()
            return HttpResponseRedirect('/country/view/')
    else:
        form = CountryForm()
    #return render_to_response('country.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'country.html'})


def country_delete(request, id):
    obj = Country.objects.get(id=id)
    del_logging(obj)
    obj.delete() 
    return HttpResponseRedirect('/country/view/')


def country_del(request, id):
    obj = Country.objects.get(id=id)
    obj.delete()
    return HttpResponseRedirect('/country/view/')
    #list = Country.objects.all()
    #return render_to_response('country_list.html', {'countries': list})


def country_list(request):
    list = Country.objects.all()
    #return render_to_response('country_list.html', {'countries': list})
    return render_to_response('index.html', {'countries': list, 'weblink': 'country_list.html'})


# ----------------- Bank --------------------

def bank_add(request):
    if request.method == 'POST':
        form = BankForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            Bank(name=name).save()
            return HttpResponseRedirect('/bank/view/')
    else:
        form = BankForm()
    #return render_to_response('bank.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bank.html'})


def bank_del(request, id):
    obj = Bank.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bank/view/')
    

def bank_list(request):
    list = Bank.objects.all()
    #return render_to_response('bank_list.html', {'banks': list})
    return render_to_response('index.html', {'banks': list, 'weblink': 'bank_list.html'})


# ----------- Bicycle --------------

def bicycle_type_add(request):
    if request.method == 'POST':
        form = BicycleTypeForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            description = form.cleaned_data['description']
            Bicycle_Type(type=type, description=description).save()
            return HttpResponseRedirect('/bicycle-type/view/')
    else:
        form = BicycleTypeForm()
    #return render_to_response('bicycle_type.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_type.html'})


def bicycle_type_del(request, id):
    obj = Bicycle_Type.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle-type/view/')


def bicycle_type_list(request):
    list = Bicycle_Type.objects.all()
    #return render_to_response('bicycle_type_list.html', {'types': list.values()})
    return render_to_response('index.html', {'types': list.values(), 'weblink': 'bicycle_type_list.html'})


def bicycle_framesize_add(request):
    if request.method == 'POST':
        form = BicycleFrameSizeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            cm = form.cleaned_data['cm']
            inch = form.cleaned_data['inch']
            FrameSize(name=name, cm=cm, inch=inch).save()
            return HttpResponseRedirect('/bicycle-framesize/view/')
    else:
        form = BicycleFrameSizeForm()
    #return render_to_response('bicycle_framesize.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_framesize.html'})


def bicycle_framesize_del(request, id):
    obj = FrameSize.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle-framesize/view/')


def bicycle_framesize_list(request):
    list = FrameSize.objects.all()
    #return render_to_response('bicycle_framesize_list.html', {'framesizes': list.values_list()})
    return render_to_response('index.html', {'framesizes': list.values_list(), 'weblink': 'bicycle_framesize_list.html'})


from django.conf import settings

def processUploadedImage(file, dir=''): 
#    img = Image.open(file) 
#    downsampleUploadedimage(img) 
#    stampUploadedImage(img) 
#    img.save(file, "JPEG") 
    upload_suffix = 'upload/' + dir + file.name
    upload_path = settings.MEDIA_ROOT + 'upload/' + file.name
        
    destination = open(settings.MEDIA_ROOT + '/upload/'+ dir + file.name, 'wb+')
    #destination = open('/media/upload/'+file.name, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()        
    return upload_suffix


def bicycle_add(request):
    if request.method == 'POST':
        form = BicycleForm(request.POST, request.FILES)
        if form.is_valid():
            #bicycle = form.save()
            model = form.cleaned_data['model']
            type = form.cleaned_data['type']
            brand = form.cleaned_data['brand']
            color = form.cleaned_data['color']
            photo = form.cleaned_data['photo']

            weight = form.cleaned_data['weight']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            #processUploadedImage(request.FILES['photo']) 
            #photo = photo,
            upload_path = processUploadedImage(photo) 
            #handle_uploaded_file(photo)
            Bicycle(model = model, type=type, brand = brand, color = color, photo=upload_path, weight = weight, price = price, currency = currency, description=description).save()
            return HttpResponseRedirect('/bicycle/view/')
            #return HttpResponseRedirect(bicycle.get_absolute_url())
    else:
        form = BicycleForm()

    #return render_to_response('bicycle.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle.html'})
    #context = {'form': form, }
    #return direct_to_template(request, 'bicycle.html', extra_context=context)
    


def bicycle_del(request, id):
    obj = Bicycle.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle/view/')


def bicycle_list(request):
    list = Bicycle.objects.all()
    #return render_to_response('bicycle_list.html', {'bicycles': list.values_list()})
    return render_to_response('index.html', {'bicycles': list.values_list(), 'weblink': 'bicycle_list.html'})


def bicycle_store_add(request):
    if request.method == 'POST':
        form = BicycleStoreForm(request.POST)
        if form.is_valid():
            model = form.cleaned_data['model']
            serial_number = form.cleaned_data['serial_number']
            size = form.cleaned_data['size']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            realization = form.cleaned_data['realization']
            count = form.cleaned_data['count']
            Bicycle_Store(model = model, serial_number=serial_number, size = size, price = price, currency = currency, description=description, realization=realization, count=count).save()
            return HttpResponseRedirect('/bicycle-store/view/')
    else:
        form = BicycleStoreForm()
    #return render_to_response('bicycle_store.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_store.html'})


def bicycle_store_del(request, id):
    obj = Bicycle_Store.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle-store/view/')


def bicycle_store_list(request):
    list = Bicycle_Store.objects.all()
    #return render_to_response('bicycle_store_list.html', {'bicycles': list.values_list()})
    return render_to_response('index.html', {'bicycles': list.values_list(), 'weblink': 'bicycle_store_list.html'})


def bicycle_sale_add(request):
    if request.method == 'POST':
        form = BicycleSaleForm(request.POST)
        if form.is_valid():
            model = form.cleaned_data['model']
            client = form.cleaned_data['client']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            date = form.cleaned_data['date']
            service = form.cleaned_data['service']
            description = form.cleaned_data['description']
            Bicycle_Sale(model = model, client=client, price = price, currency = currency, date=date, service=service, description=description).save()
            
            update_bicycle = Bicycle_Store.objects.get(id=model.id)
            update_bicycle.count = 0
            update_bicycle.save()
            
            update_client = Client.objects.get(id=client.id)
            update_client.summ = update.summ + price 
            update_client.save()
            
            return HttpResponseRedirect('/bicycle/sale/view/')
    else:
        form = BicycleSaleForm()
    #return render_to_response('bicycle_store.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_sale.html'})


def bicycle_sale_del(request, id):
    obj = Bicycle_Sale.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle/sale/view/')


def bicycle_sale_list(request):
    list = Bicycle_Sale.objects.all()
    return render_to_response('index.html', {'bicycles': list.values_list(), 'weblink': 'bicycle_sale_list.html'})

# --------------------Dealer company ------------------------
def dealer_add(request):
    if request.method == 'POST':
        form = DealerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            street = form.cleaned_data['street']
            www = form.cleaned_data['www']
            description = form.cleaned_data['description']
            director = form.cleaned_data['director']
            Dealer(name=name, country=country, city=city, street=street, www=www, description=description, director=director).save()
            return HttpResponseRedirect('/dealer/view/')
    else:
        form = DealerForm()
    #return render_to_response('dealer.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer.html'})

 
def dealer_del(request, id):
    obj = Dealer.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer/view/')
 
 
def dealer_list(request):
    list = Dealer.objects.all()
    #return render_to_response('dealer_list.html', {'dealers': list.values_list()})
    return render_to_response('index.html', {'dealers': list.values_list(), 'weblink': 'dealer_list.html'})


def dealer_manager_add(request):
    if request.method == 'POST':
        form = DealerManagerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            company = form.cleaned_data['company']
            description = form.cleaned_data['description']
            DealerManager(name=name, email=email, phone=phone, company=company, description=description).save()
            return HttpResponseRedirect('/dealer-manager/view/')
    else:
        form = DealerManagerForm()
    #return render_to_response('dealer-manager.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer-manager.html'})

 
def dealer_manager_del(request, id):
    obj = DealerManager.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer-manager/view/')
 
 
def dealer_manager_list(request):
    list = DealerManager.objects.all()
    #return render_to_response('dealer-manager_list.html', {'dealer_managers': list.values_list()})
    return render_to_response('index.html', {'dealer_managers': list.values_list(), 'weblink': 'dealer-manager_list.html'})


def dealer_payment_add(request):
    if request.method == 'POST':
        form = DealerPaymentForm(request.POST)
        if form.is_valid():
            invoice_number = form.cleaned_data['invoice_number']
            date = form.cleaned_data['date']
            bank = form.cleaned_data['bank']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            DealerPayment(invoice_number=invoice_number, date=date, bank=bank, price=price, currency=currency, description=description).save()
            return HttpResponseRedirect('/dealer/payment/view/')
    else:
        form = DealerPaymentForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer_payment.html'})

 
def dealer_payment_del(request, id):
    obj = DealerPayment.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer/payment/view/')
 
 
def dealer_payment_list(request):
    list = DealerPayment.objects.all()
    return render_to_response('index.html', {'dealer_payment': list.values_list(), 'weblink': 'dealer_payment_list.html'})


def dealer_invoice_add(request):
    if request.method == 'POST':
        form = DealerInvoiceForm(request.POST)
        if form.is_valid():
            origin_id = form.cleaned_data['origin_id']
            date = form.cleaned_data['date']
            company = form.cleaned_data['company']
            manager = form.cleaned_data['manager']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            file = form.cleaned_data['file']
            received = form.cleaned_data['received']
            payment = form.cleaned_data['payment']
            description = form.cleaned_data['description']
            DealerInvoice(origin_id=origin_id, date=date, company=company, manager=manager, price=price, currency=currency, file=file, received=received, payment=payment, description=description).save()
            return HttpResponseRedirect('/dealer/invoice/view/')
    else:
        form = DealerInvoiceForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer_invoice.html'})

 
def dealer_invoice_del(request, id):
    obj = DealerInvoice.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer/invoice/view/')
 
 
def dealer_invoice_list(request):
    list = DealerInvoice.objects.all()
    return render_to_response('index.html', {'dealer_invoice': list.values_list(), 'weblink': 'dealer_invoice_list.html'})


# --------------- Classification ---------

def category_list(request):
    list = Type.objects.all()
    #return render_to_response('category_list.html', {'categories': list.values_list()})
    return render_to_response('index.html', {'categories': list.values_list(), 'weblink': 'category_list.html'})

def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            Type(name=name, description=description).save()
            return HttpResponseRedirect('/category/view/')
    else:
        form = CategoryForm()
    #return render_to_response('category.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'category.html'})


def category_del(request, id):
    obj = Type.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/category/view/')    

# -------------- Currency and operations ----------------------
def curency_add(request):
    if request.method == 'POST':
        form = CurencyForm(request.POST)
        if form.is_valid():
            ids = form.cleaned_data['ids']
            ids_char = form.cleaned_data['ids_char']
            name = form.cleaned_data['name']
            country = form.cleaned_data['country']
            Currency(ids=ids, ids_char=ids_char, name=name, country=country).save()
            return HttpResponseRedirect('/curency/view/')
    else:
        form = CurencyForm()
    #return render_to_response('curency.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'curency.html'})


def curency_list(request):
    list = Currency.objects.all()
    #return render_to_response('curency_list.html', {'currency': list.values()})
    return render_to_response('index.html', {'currency': list.values(), 'weblink': 'curency_list.html'})


def curency_del(request, id):
    obj = Currency.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/curency/view/')


def exchange_add(request):
    if request.method == 'POST':
        form = ExchangeForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            currency = form.cleaned_data['currency']
            value = form.cleaned_data['value']
            Exchange(date=date, currency=currency, value=value).save()
            return HttpResponseRedirect('/exchange/view/')
    else:
        form = ExchangeForm()
    #return render_to_response('exchange.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'exchange.html'})


def exchange_list(request):
    list = Exchange.objects.all()
    #return render_to_response('exchange_list.html', {'exchange': list.values()})
    return render_to_response('index.html', {'exchange': list.values(), 'weblink': 'exchange_list.html'})


def exchange_del(request, id):
    obj = Exchange.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/exchange/view/')



# -------- Catalog ---------------- 

def manufacturer_add(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            www = form.cleaned_data.get('www')
            country = form.cleaned_data.get('country')
            logo = form.cleaned_data.get('logo')
            upload_path = processUploadedImage(logo, 'manufecturer/') 
            #country = SelectFromModel(objects=Country.objects.all())
            Manufacturer(name=name, description=description, www=www, logo=upload_path, country=country).save()
            return HttpResponseRedirect('/manufacturer/view/')
    else:
        form = ManufacturerForm()
    #return render_to_response('manufacturer.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'manufacturer.html'})


def manufaturer_list(request):
    list = Manufacturer.objects.all()
    #return render_to_response('manufacturer_list.html', {'manufactures': list.values_list()})
    return render_to_response('index.html', {'manufactures': list.values_list(), 'weblink': 'manufacturer_list.html'})


def manufacturer_delete(request, id):
    obj = Manufacturer.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/manufacturer/view/')



def catalog_add(request):
    if request.method == 'POST':
        form = CatalogForm(request.POST, request.FILES)
        if form.is_valid():
            ids = form.cleaned_data['ids']
            name = form.cleaned_data['name']
            manufacturer = form.cleaned_data['manufacturer']
            type = form.cleaned_data['type']
            size = form.cleaned_data['size']
            weight = form.cleaned_data['weight']
            photo = form.cleaned_data['photo']
            year = form.cleaned_data['year']
            sale = form.cleaned_data['sale']
            sale_to = form.cleaned_data['sale_to']
            color = form.cleaned_data['color']
            country = form.cleaned_data['country']
            description = form.cleaned_data['description']               
            upload_path = processUploadedImage(photo, 'catalog/') 
            Catalog(ids=ids, name=name, manufacturer=manufacturer, type=type, size=size, weight=weight, year=year, sale=sale, sale_to=sale_to, color=color, description=description, photo=upload_path, country=country).save()
            return HttpResponseRedirect('/catalog/view/')
    else:
        form = CatalogForm()
    #return render_to_response('catalog.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'catalog.html'})


def catalog_list(request):
    list = Catalog.objects.all()
    #return render_to_response('catalog_list.html', {'catalog': list.values_list()})
    return render_to_response('index.html', {'catalog': list.values_list(), 'weblink': 'catalog_list.html'})


def catalog_delete(request, id):
    obj = Catalog.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/catalog/view/')


# ------------- Clients -------------
def client_add(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            forumname = form.cleaned_data['forumname']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            sale = form.cleaned_data['sale']
            summ = form.cleaned_data['summ']
            description = form.cleaned_data['description']
 
            Client(name=name, forumname=forumname, country=country, city=city, email=email, phone=phone, sale=sale, summ=summ, description=description).save()
            return HttpResponseRedirect('/client/view/')
    else:
        form = ClientForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'client.html'})


def client_list(request):
    list = Client.objects.all()
    return render_to_response('index.html', {'clients': list.values_list(), 'weblink': 'client_list.html'})


def client_delete(request, id):
    obj = Client.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/client/view/')



def clientdebts_add(request):
    if request.method == 'POST':
        form = ClientDebtsForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            ClientDebts(client=client, date=date, price=price, description=description).save()
            return HttpResponseRedirect('/clientdebts/view/')
    else:
        form = ClientDebtsForm()
    #return render_to_response('clientdebts.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'clientdebts.html'})


def clientdebts_list(request):
    list = ClientDebts.objects.select_related().all()
    return render_to_response('index.html', {'clients': list.values_list(), 'weblink': 'clientdebts_list.html'})


def clientdebts_delete(request, id):
    obj = ClientDebts.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/clientdebts/view/')


def clientcredits_add(request):
    if request.method == 'POST':
        form = ClientCreditsForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            ClientCredits(client=client, date=date, price=price, description=description).save()
            return HttpResponseRedirect('/clientcredits/view/')
    else:
        form = ClientCreditsForm()
    #return render_to_response('clientcredits.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'clientcredits.html'})


def clientcredits_list(request):
    list = ClientCredits.objects.all()
    return render_to_response('index.html', {'clients': list.values_list(), 'weblink': 'clientcredits_list.html'})


def clientcredits_delete(request, id):
    obj = ClientCredits.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/clientcredits/view/')


from django.db import connection

def search_client_id(request):
    #query = request.GET.get('q', '')
    return render_to_response('index.html', {'weblink': 'client_id_search.html'})


def client_result(request):
    
    user = request.GET['id'] 
    sql1 = "SELECT sum(price) FROM accounting_clientcredits WHERE client_id = %s;"
    sql2 = "SELECT sum(price) FROM accounting_clientdebts WHERE client_id = %s;"
    #user = id;
    try:
        cursor = connection.cursor()
        cursor.execute(sql1, [user])   
        credit= cursor.fetchone()
    
        cursor.execute(sql2, [user])
        debts = cursor.fetchone()
    
        if (credit[0] is None):
            credit = (0,)
        elif (debts[0] is None):
            debts = (0,)
    
        res = credit[0] - debts[0]
        
    except TypeError:
        res = "Такого клієнта не існує"
    
    try:
        client_name = Client.objects.values('name', 'forumname').get(id=user)
    except ObjectDoesNotExist:
        client_name = ""
    
    #list_credit = ClientCredits.objects.values('client', 'price').filter(client="2")
    #list_debt = ClientDebts.objects.filter(client='2').values("client", "price").select_related('client')
    #list_debt = ClientDebts.objects.filter(client='2').select_related('client')
    #list_debt = ClientDebts.objects.filter(client='2').annotate(Sum("price"))
    #return render_to_response('index.html', {'clients': list_credit.values_list(), 'weblink': 'client_result.html'})
    #return render_to_response('index.html', {'clients': list_debt.values_list(), 'weblink': 'client_result.html'})
    return render_to_response('index.html', {'clients': res, 'weblink': 'client_result.html', 'client_name': client_name})


# --------------- WorkShop -----------------
def workgroup_add(request):
    if request.method == 'POST':
        form = WorkGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            WorkGroup(name=name, description=description).save()
            return HttpResponseRedirect('/workgroup/view/')
    else:
        form = WorkGroupForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'workgroup.html'})


def workgroup_list(request):
    list = WorkGroup.objects.all()
    return render_to_response('index.html', {'workgroups': list.values_list(), 'weblink': 'workgroup_list.html'})


def workgroup_delete(request, id):
    obj = WorkGroup.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/workgroup/view/')


def worktype_add(request):
    if request.method == 'POST':
        form = WorkTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            work_group = form.cleaned_data['work_group']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            WorkType(name=name, work_group=work_group, price=price, description=description).save()
            return HttpResponseRedirect('/worktype/view/')
    else:
        form = WorkTypeForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'worktype.html'})


def worktype_list(request):
    list = WorkType.objects.all()
    return render_to_response('index.html', {'worktypes': list.values_list(), 'weblink': 'worktype_list.html'})


def worktype_delete(request, id):
    obj = WorkType.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/worktype/view/')


def workstatus_add(request):
    if request.method == 'POST':
        form = WorkStatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            WorkStatus(name=name, description=description).save()
            return HttpResponseRedirect('/workstatus/view/')
    else:
        form = WorkStatusForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'workstatus.html'})


def workstatus_list(request):
    list = WorkStatus.objects.all()
    return render_to_response('index.html', {'workstatus': list.values_list(), 'weblink': 'workstatus_list.html'})


def workstatus_delete(request, id):
    obj = WorkStatus.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/workstatus/view/')


def workticket_add(request):
    if request.method == 'POST':
        form = WorkTicketForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            end_date = form.cleaned_data['end_date']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            WorkTicket(client=client, date=date, end_date=end_date, status=status, description=description).save()
            return HttpResponseRedirect('/workticket/view/')
    else:
        form = WorkTicketForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'workticket.html'})


def workticket_list(request):
    list = WorkTicket.objects.all()
    return render_to_response('index.html', {'workticket': list, 'weblink': 'workticket_list.html'})


def workticket_delete(request, id):
    obj = WorkTicket.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/workticket/view/')


def workshop_add(request):
    if request.method == 'POST':
        form = WorkShopForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            work_type = form.cleaned_data['work_type']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            WorkShop(client=client, date=date, work_type=work_type, price=price, description=description).save()
            return HttpResponseRedirect('/workshop/view/')
    else:
        form = WorkShopForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'workshop.html'})


def workshop_list(request):
    list = WorkShop.objects.all()
    return render_to_response('index.html', {'workshop': list, 'weblink': 'workshop_list.html'})


def workshop_delete(request, id):
    obj = WorkShop.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/workshop/view/')


#--------------------- MY Costs -------------------------
def costtype_add(request):
    if request.method == 'POST':
        form = CostTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            CostType(name=name, description=description).save()
            return HttpResponseRedirect('/cost/type/view/')
    else:
        form = CostTypeForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'costtype.html'})


def costtype_list(request):
    list = CostType.objects.all()
    return render_to_response('index.html', {'costtypes': list.values_list(), 'weblink': 'costtype_list.html'})


def costtype_delete(request, id):
    obj = CostType.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/cost/type/view/')


def cost_add(request):
    if request.method == 'POST':
        form = CostsForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            cost_type = form.cleaned_data['cost_type']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            Costs(date=date, cost_type=cost_type, price=price, description=description).save()
            return HttpResponseRedirect('/cost/view/')
    else:
        form = CostsForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'cost.html'})


def cost_list(request):
    list = Costs.objects.all()
    return render_to_response('index.html', {'costs': list.values_list(), 'weblink': 'cost_list.html'})


def cost_delete(request, id):
    obj = Costs.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/cost/view/')