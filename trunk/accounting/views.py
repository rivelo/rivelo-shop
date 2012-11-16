# -*- coding: utf-8 -*-

from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import resolve

from models import Manufacturer, Country, Type, Currency, Bicycle_Type, Bicycle,  FrameSize, Bicycle_Store, Bicycle_Sale, Bicycle_Order
from forms import ContactForm, ManufacturerForm, CountryForm, CurencyForm, CategoryForm, BicycleTypeForm, BicycleForm, BicycleFrameSizeForm, BicycleStoreForm, BicycleSaleForm, BicycleOrderForm, BicycleSaleEditForm, BicycleOrderEditForm 

from models import Catalog, Client, ClientDebts, ClientCredits, ClientInvoice 
from forms import CatalogForm, ClientForm, ClientDebtsForm, ClientCreditsForm, ClientInvoiceForm

from models import Dealer, DealerManager, DealerManager, DealerPayment, DealerInvoice, InvoiceComponentList, Bank, Exchange, PreOrder
from forms import DealerManagerForm, DealerForm, DealerPaymentForm, DealerInvoiceForm, InvoiceComponentListForm, BankForm, ExchangeForm, PreOrderForm, InvoiceComponentForm

from models import WorkGroup, WorkType, WorkShop, WorkStatus, WorkTicket, CostType, Costs, ShopDailySales
from forms import WorkGroupForm, WorkTypeForm, WorkShopForm, WorkStatusForm, WorkTicketForm, CostTypeForm, CostsForm, ShopDailySalesForm
  
from django.http import HttpResponseRedirect, HttpRequest, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth

from django.http import HttpResponse 
from django.http import Http404  

from django.conf import settings
import datetime
import calendar

from django.db.models import Sum, Count

from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pytils_ua

now = datetime.datetime.now()


def custom_proc(request):
# "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'Rivelo catalog',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }

    
def auth_group(user, group):
    return True if user.groups.filter(name=group) else False


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


def del_logging(obj):
    file_name = 'test_log'
    log_path = settings.MEDIA_ROOT + 'logs/' + file_name + '.log'
    log_file = open(log_path, 'a')
    #for s in obj:
    #    result = result + ' | ' + s 
    #log_file.write("DELETE FROM TABLE " + table_name + " WHERE id = " + obj.name + "\n")
    log_file.write("%s >>> DELETE FROM TABLE %s WHERE id = %s \n" % (str(datetime.datetime.now()), obj._meta.verbose_name, obj.id) )
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


# ------------ Country -----------------

def country_add(request):
    a = Country()
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=a)
        if form.is_valid():
            name = form.cleaned_data['name']
            Country(name=name).save()
            return HttpResponseRedirect('/country/view/')
    else:
        form = CountryForm(instance = a)
    return render_to_response('index.html', {'form': form, 'weblink': 'country.html', 'next': current_url}, context_instance=RequestContext(request, processors=[custom_proc]))


def country_del(request, id):
    if auth_group(request.user, 'admin')==False:
        return HttpResponseRedirect('/country/view/')
    obj = Country.objects.get(id=id)
    del_logging(obj)
    obj.delete() 
    return HttpResponseRedirect('/country/view/')


def country_edit(request, id):
    a = Country.objects.get(pk=id)
    current_url = request.get_full_path()
    if request.method == 'POST':
        form = CountryForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/country/view/')
    else:
        form = CountryForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'country.html', 'next': current_url}, context_instance=RequestContext(request, processors=[custom_proc]))


def country_list(request):
    current_url = request.get_full_path()
    list = Country.objects.all()
    #return render_to_response('country_list.html', {'countries': list})
    return render_to_response('index.html', {'countries': list, 'weblink': 'country_list.html', 'next': current_url}, context_instance=RequestContext(request, processors=[custom_proc]))


# ----------------- Bank --------------------

def bank_add(request):
    a = Bank()
    if request.method == 'POST':
        form = BankForm(request.POST, instance=a)
        if form.is_valid():
            name = form.cleaned_data['name']
            Bank(name=name).save()
            return HttpResponseRedirect('/bank/view/')
    else:
        form = BankForm(instance=a)
    #return render_to_response('bank.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bank.html', 'text': 'Додати новий банк'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bank_edit(request, id):
    a = Bank.objects.get(pk=id)
    if request.method == 'POST':
        form = BankForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bank/view/')
    else:
        form = BankForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'bank.html', 'text': 'Редагувати банк'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bank_del(request, id):
    if auth_group(request.user, 'admin')==False:
        return HttpResponseRedirect('/bank/view/')
    obj = Bank.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bank/view/')
    

def bank_list(request):
    list = Bank.objects.all()
    #return render_to_response('bank_list.html', {'banks': list})
    return render_to_response('index.html', {'banks': list, 'weblink': 'bank_list.html'}, context_instance=RequestContext(request, processors=[custom_proc]))


# ----------- Bicycle --------------

def bicycle_type_add(request):
    a = Bicycle_Type()
    if request.method == 'POST':
        form = BicycleTypeForm(request.POST, instance=a)
        if form.is_valid():
            type = form.cleaned_data['type']
            description = form.cleaned_data['description']
            Bicycle_Type(type=type, description=description).save()
            return HttpResponseRedirect('/bicycle-type/view/')
    else:
        form = BicycleTypeForm(instance=a)
    #return render_to_response('bicycle_type.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_type.html'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_type_edit(request, id):
    a = Bicycle_Type.objects.get(pk=id)
    if request.method == 'POST':
        form = BicycleTypeForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bicycle-type/view/')
    else:
        form = BicycleTypeForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_type.html', 'text': 'Редагувати тип'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_type_del(request, id):
    if auth_group(request.user, 'admin') == False:
        return HttpResponseRedirect('/bicycle-type/view/')
    obj = Bicycle_Type.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle-type/view/')


def bicycle_type_list(request):
    list = Bicycle_Type.objects.all()
    return render_to_response('index.html', {'types': list.values(), 'weblink': 'bicycle_type_list.html'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_framesize_add(request):
    a = FrameSize()
    if request.method == 'POST':
        form = BicycleFrameSizeForm(request.POST, instance=a)
        if form.is_valid():
            name = form.cleaned_data['name']
            cm = form.cleaned_data['cm']
            inch = form.cleaned_data['inch']
            FrameSize(name=name, cm=cm, inch=inch).save()
            return HttpResponseRedirect('/bicycle-framesize/view/')
    else:
        form = BicycleFrameSizeForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_framesize.html', 'text': 'Створення нового розміру рами'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_framesize_edit(request, id):
    a = FrameSize.objects.get(pk=id)
    if request.method == 'POST':
        form = BicycleFrameSizeForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bicycle-framesize/view/')
    else:
        form = BicycleFrameSizeForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_framesize.html', 'text': 'Розмір рами (редагування)'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_framesize_del(request, id):
    if auth_group(request.user, 'admin') == False:
        return HttpResponseRedirect('/bicycle-framesize/view/')
    obj = FrameSize.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle-framesize/view/')


def bicycle_framesize_list(request):
    list = FrameSize.objects.all()
    #return render_to_response('bicycle_framesize_list.html', {'framesizes': list.values_list()})
    return render_to_response('index.html', {'framesizes': list, 'weblink': 'bicycle_framesize_list.html'}, context_instance=RequestContext(request, processors=[custom_proc]))


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
    if (auth_group(request.user, 'seller') or auth_group(request.user, 'admin')) == False:
        return HttpResponseRedirect('/bicycle/view/')
    
    a = Bicycle(year=datetime.date.today())
    if request.method == 'POST':
        form = BicycleForm(request.POST, request.FILES, instance=a)
        if form.is_valid():
            #bicycle = form.save()
            model = form.cleaned_data['model']
            type = form.cleaned_data['type']
            brand = form.cleaned_data['brand']
            color = form.cleaned_data['color']
            photo = form.cleaned_data['photo']
            year = form.cleaned_data['year']
            weight = form.cleaned_data['weight']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            #processUploadedImage(request.FILES['photo']) 
            #photo = photo,
            upload_path = processUploadedImage(photo) 
            #handle_uploaded_file(photo)
            Bicycle(model = model, type=type, brand = brand, color = color, photo=upload_path, weight = weight, price = price, currency = currency, description=description, year=year).save()
            return HttpResponseRedirect('/bicycle/view/')
            #return HttpResponseRedirect(bicycle.get_absolute_url())
    else:
        form = BicycleForm(instance=a)

    #return render_to_response('bicycle.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle.html', 'text': 'Велосипед з каталогу (створення)'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_edit(request, id):
    if (auth_group(request.user, 'seller') or auth_group(request.user, 'admin')) == False:
        return HttpResponseRedirect('/bicycle/view/')
    
    a = Bicycle.objects.get(pk=id)
    if request.method == 'POST':
        form = BicycleForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bicycle/view/')
    else:
        form = BicycleForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle.html', 'text': 'Велосипед з каталогу (редагування)'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_del(request, id):
    if auth_group(request.user, 'admin') == False:
        return HttpResponseRedirect('/bicycle/view/')
    obj = Bicycle.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle/view/')


def bicycle_list(request, year=None, brand=None, percent=None):
    #yyy = None
    if year == None:
        now = datetime.datetime.now()
        year = now.year
    if brand == None:
        list = Bicycle.objects.filter(year__year=year)
    else:
        list = Bicycle.objects.filter(year__year=year, brand=brand)
        if percent!=None:
            Bicycle.objects.filter(year__year=year, brand=brand).update(sale=percent)
    bike_company = Bicycle.objects.filter(year__year=year).values('brand', 'brand__name').annotate(num_company=Count('model'))
    #return render_to_response('bicycle_list.html', {'bicycles': list.values_list()})
    return render_to_response('index.html', {'bicycles': list, 'year': year, 'b_company': bike_company, 'sale': percent, 'weblink': 'bicycle_list.html'}, context_instance=RequestContext(request, processors=[custom_proc]))


def bicycle_all_list(request):
    list = Bicycle.objects.all()
    #return render_to_response('bicycle_list.html', {'bicycles': list.values_list()})
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_list.html'})


def bicycle_photo(request, id):
    obj = Bicycle.objects.get(id=id)
    #return render_to_response('bicycle_list.html', {'bicycles': list.values_list()})
    return render_to_response('index.html', {'bicycle': obj, 'weblink': 'bicycle_photo.html'})


def bicycle_store_add(request, id=None):
    bike = None
    if id != None:
        bike = Bicycle.objects.get(id=id)
        
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
            date = form.cleaned_data['date']
            Bicycle_Store(model = model, serial_number=serial_number, size = size, price = price, currency = currency, description=description, realization=realization, count=count, date=date).save()
            return HttpResponseRedirect('/bicycle-store/view/seller/')
    else:
        if bike != None:
            form = BicycleStoreForm(initial={'model': bike.id, 'count': '1'})
        else:
            form = BicycleStoreForm()
    #return render_to_response('bicycle_store.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_store.html'})


def bicycle_store_edit(request, id):
    a = Bicycle_Store.objects.get(pk=id)
    if request.method == 'POST':
        form = BicycleStoreForm(request.POST, instance=a)
        if form.is_valid():
#===============================================================================
#            model = form.cleaned_data['model']
#            serial_number = form.cleaned_data['serial_number']
#            size = form.cleaned_data['size']
#            price = form.cleaned_data['price']
#            currency = form.cleaned_data['currency']
#            description = form.cleaned_data['description']
#            realization = form.cleaned_data['realization']
#            count = form.cleaned_data['count']
#            date = form.cleaned_data['date']            
#            Bicycle_Store(id = id, model = model, serial_number=serial_number, size = size, price = price, currency = currency, description=description, realization=realization, count=count, date=date).save()
#===============================================================================
            form.save()
            return HttpResponseRedirect('/bicycle-store/view/seller/')
    else:
        form = BicycleStoreForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_store.html', 'text': 'Редагувати тип'})


def bicycle_store_del(request, id):
    obj = Bicycle_Store.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle-store/view/seller/')


def bicycle_store_list(request, all=False):
    list = None
    if all==True:
        list = Bicycle_Store.objects.all()
    else:
        list = Bicycle_Store.objects.filter(count=1)
    price_summ = 0
    real_summ = 0
    bike_summ = 0
    for item in list:
        if item.count != 0:
            price_summ = price_summ + item.price * item.count 
        real_summ = real_summ + item.realization
        bike_summ = bike_summ + item.count
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_store_list.html', 'price_summ': price_summ, 'real_summ': real_summ, 'bike_summ': bike_summ})


def bicycle_store_list_by_seller(request, all=False, size='all', year='all', brand='all', html=False):
    list = None
    if all==True:
        if brand == 'all':
            list = Bicycle_Store.objects.all()
        else:
            list = Bicycle_Store.objects.filter(count=1, model__brand=brand)
    else:
        if size == 'all':
            if year == 'all':
                list = Bicycle_Store.objects.filter(count=1)
            else:
                list = Bicycle_Store.objects.filter(count=1, model__year__year=year)
        else:
            if year == 'all':
                list = Bicycle_Store.objects.filter(count=1, size=size)
            else:
                list = Bicycle_Store.objects.filter(count=1, model__year__year=year, size=size)
            #list = Bicycle_Store.objects.filter(count=1, size=size)
        
    price_summ = 0
    real_summ = 0
    bike_summ = 0
    for item in list:
        if item.count != 0:
            price_summ = price_summ + item.price * item.count 
        real_summ = real_summ + item.realization
        bike_summ = bike_summ + item.count
    frames = FrameSize.objects.all()
    bike_company = Bicycle_Store.objects.filter(count=1).values('model__brand', 'model__brand__name').annotate(num_company=Count('count'))
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_store_list_by_seller.html', 'price_summ': price_summ, 'real_summ': real_summ, 'bike_summ': bike_summ, 'sizes': frames, 'b_company': bike_company, 'html': html})


def bicycle_store_search(request):
    return render_to_response('index.html', {'weblink': 'frame_search.html'})


def bicycle_store_search_result(request, all=False):
    list = None
    serial = request.GET['serial_number']
    if all==True:
        list = Bicycle_Store.objects.all()
    else:
        list = Bicycle_Store.objects.filter(serial_number__icontains=serial)
    price_summ = 0
    real_summ = 0
    bike_summ = 0
    for item in list:
        if item.count != 0:
            price_summ = price_summ + item.price * item.count 
        real_summ = real_summ + item.realization
        bike_summ = bike_summ + item.count
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_store_list_by_seller.html', 'price_summ': price_summ, 'real_summ': real_summ, 'bike_summ': bike_summ})


def bicycle_store_price(request):
    list = Bicycle_Store.objects.filter(count=1)
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_shop_price_list.html', 'view':True})


def bicycle_store_price_print(request):
    list = Bicycle_Store.objects.filter(count=1)
    return render_to_response('bicycle_shop_price_list.html', {'bicycles': list, 'view':False})


def store_report_bysize(request, id):
    list = Bicycle_Store.objects.filter(size = id, count = 1)
    frame = FrameSize.objects.get(id=id)
    frame_str = u"Розмір рами " + frame.name
    frames = FrameSize.objects.all()
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_store_list.html', 'text': frame_str, 'sizes': frames})

    
def store_report_bytype(request, id):
    #list = Bicycle.objects.filter(type=id)
    list = Bicycle_Store.objects.filter(model__type__exact=id, count__gt=0)
    #frame = Bicycle_Type.objects.get(id=id)
    type = list[0].model.type.type
    #text = u"Тип велосипеду: " + frame.type
    text = u"Тип велосипеду: " + type
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_store_list_by_seller.html', 'text': text})


def bicycle_sale_add(request, id=None):
    bike = None
    serial_number = ''
    if id != None:
        bike = Bicycle_Store.objects.get(id=id)
        serial_number = bike.serial_number
        
    if request.method == 'POST':
        form = BicycleSaleForm(request.POST, initial={'currency': 3})
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
            if update_bicycle.count != 0: 
                update_bicycle.count = update_bicycle.count - 1 
            #update_bicycle.count - 1
            update_bicycle.save()
            
            update_client = Client.objects.get(id=client.id)
            update_client.summ = update_client.summ + price 
            update_client.save()
            
            ClientDebts(client=client, date=date, price=price, description=""+str(model)).save()
            redirect = "/client/result/search/?id="+str(client.id)
            return HttpResponseRedirect(redirect)
    else:
        if bike != None:
            form = BicycleSaleForm(initial={'model': bike.id, 'price': bike.model.price, 'currency': bike.model.currency.id})
        else:
            form = BicycleSaleForm(initial={'currency': 3})
    
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_sale.html', 'serial_number': serial_number, 'text': 'Продаж велосипеду'})


def bicycle_sale_edit(request, id):
    a = Bicycle_Sale.objects.get(pk=id)
    
    if request.method == 'POST':
        form = BicycleSaleEditForm(request.POST, instance=a, bike_id=a.model.model.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bicycle/sale/view/')
    else:
        form = BicycleSaleEditForm(instance=a, bike_id=a.model.model.id)
        
    serial_number = a.model.serial_number
    #serial_number = "test number"
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_sale.html', 'text': 'Редагувати проданий велосипед', 'serial_number': serial_number})


def bicycle_sale_del(request, id):
    obj = Bicycle_Sale.objects.get(id=id)
    del_logging(obj)
    update_client = Client.objects.get(id=obj.client.id)
    update_client.summ = update_client.summ - obj.price 
    update_client.save()
    update_storebike = Bicycle_Store.objects.get(id=obj.model.id)
    update_storebike.count = update_storebike.count + 1
    update_storebike.save()
    obj.delete()
    return HttpResponseRedirect('/bicycle/sale/view/')


def bicycle_sale_list(request, year=False, month=False, id=None):
    list = None
    if (year==False) & (month==False):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        #list = Bicycle_Sale.objects.all().order_by('date')
        if (id != None):
            list = Bicycle_Sale.objects.filter(model=id).order_by('date')
        else:
            list = Bicycle_Sale.objects.filter(date__year=year, date__month=month).order_by('date')
    else:
       list = Bicycle_Sale.objects.filter(date__year=year, date__month=month).order_by('date')
       
    price_summ = 0
    service_summ = 0
    for item in list:
        price_summ = price_summ + item.price
        if item.service == False:
            service_summ =  service_summ + 1
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_sale_list.html', 'price_summ':price_summ, 'service_summ':service_summ,})


def bicycle_sale_service(request, id):
    list = Bicycle_Sale.objects.get(id=id)
    list.service = True
    list.save()
    list = Bicycle_Sale.objects.filter(id=id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_sale_list.html',})


def bicycle_sale_check(request, id=None):
    list = Bicycle_Sale.objects.get(id=id)
    text = pytils_ua.numeral.in_words(int(list.price))
    month = pytils_ua.dt.ru_strftime(u"%d %B %Y", list.date, inflected=True)
    return render_to_response('index.html', {'bicycle': list, 'month':month, 'str_number':text, 'weblink': 'bicycle_sale_check.html', 'print':'True'})


def bicycle_sale_check_print(request, id=None):
    list = Bicycle_Sale.objects.get(id=id)
    text = pytils_ua.numeral.in_words(int(list.price))
    month = pytils_ua.dt.ru_strftime(u"%d %B %Y", list.date, inflected=True)
    return render_to_response('bicycle_sale_check.html', {'bicycle': list, 'month':month, 'str_number':text,})



def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    

def bicycle_sale_report(request):
    query = "SELECT EXTRACT(year FROM date) as year, EXTRACT(month from date) as month, MONTHNAME(date) as month_name, COUNT(*) as bike_count, sum(price) as s_price FROM accounting_bicycle_sale GROUP BY year,month;"
    #sql2 = "SELECT sum(price) FROM accounting_clientdebts WHERE client_id = %s;"
    #user = id;
    list = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        list = dictfetchall(cursor)
        #list = cursor.execute(sql1, )   
        
    except TypeError:
        res = "Помилка"
        
    sum = 0
    bike_sum = 0
    for month in list:
         sum = sum + month['s_price']
         bike_sum = bike_sum + month['bike_count']

    #list = Bicycle_Sale.objects.all().order_by('date')
    return render_to_response('index.html', {'bicycles': list, 'all_sum': sum, 'bike_sum': bike_sum, 'weblink': 'bicycle_sale_report.html'})


def bicycle_sale_report_by_brand(request):
    #list = Bicycle_Order.objects.annotate(bcount=Count("model")) 
    list = Bicycle_Sale.objects.annotate(bcount=Count("model__model__model")).order_by("model__model__brand")
#    objects.filter(date__year=now.year, date__month=now.month).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)", 'day': "EXTRACT(day from date)"}).values('year', 'month', 'day').annotate(suma=Sum("price")).order_by()    
    return render_to_response('index.html', {'bicycles': list, 'weblink': 'bicycle_sale_report_bybrand.html'})    


def bicycle_order_add(request):
    a = Bicycle_Order(prepay=0, sale=0, currency=Currency.objects.get(id=3))
    if request.method == 'POST':
        form = BicycleOrderForm(request.POST, instance = a)
        if form.is_valid():
            client = form.cleaned_data['client']
            model = form.cleaned_data['model']
            size = form.cleaned_data['size']
            price = form.cleaned_data['price']
            sale = form.cleaned_data['sale']
            prepay = form.cleaned_data['prepay']
            currency = form.cleaned_data['currency']
            date = form.cleaned_data['date']
            done = form.cleaned_data['done']
            description = form.cleaned_data['description']
            ClientCredits(client=client, date=date, price=prepay, description="Передоплата за "+str(model)).save()
            Bicycle_Order(client=client, model=model, size=size, price=price, sale=sale, currency=currency, date=date, done=done, description=description, prepay=prepay).save()            
            return HttpResponseRedirect('/bicycle/order/view/')
    else:
        form = BicycleOrderForm(instance = a)
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_order.html'})
    

def bicycle_order_list(request):
    list = Bicycle_Order.objects.all().order_by("-date")
    return render_to_response('index.html', {'order': list, 'weblink': 'bicycle_order_list.html'})
    

def bicycle_order_edit(request, id):
    a = Bicycle_Order.objects.get(pk=id)
    
    if request.method == 'POST':
        #form = BicycleOrderEditForm(request.POST, instance=a, bike_id=a.model.id)
        form = BicycleOrderEditForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/bicycle/order/view/')
    else:
        #form = BicycleOrderEditForm(instance=a, bike_id=a.model.id)
        form = BicycleOrderEditForm(instance=a)
   
    return render_to_response('index.html', {'form': form, 'weblink': 'bicycle_order.html'})


def bicycle_order_del(request, id):
    obj = Bicycle_Order.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/bicycle/order/view/')    


def bicycle_order_done(request, id):
    obj = Bicycle_Order.objects.get(id=id)
    obj.done = True
    obj.save()
    return HttpResponseRedirect('/bicycle/order/view/')

# --------------------Dealer company ------------------------
def dealer_add(request):
    a = Dealer()
    if request.method == 'POST':
        form = DealerForm(request.POST, instance = a)
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
        form = DealerForm(instance = a)
    #return render_to_response('dealer.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer.html'})


def dealer_edit(request, id):
    a = Dealer.objects.get(pk=id)
    if request.method == 'POST':
        form = DealerForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dealer/view/')
    else:
        form = DealerForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer.html'})

 
def dealer_del(request, id):
    obj = Dealer.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer/view/')
 
 
def dealer_list(request):
    list = Dealer.objects.all()
    #return render_to_response('dealer_list.html', {'dealers': list.values_list()})
    return render_to_response('index.html', {'dealers': list, 'weblink': 'dealer_list.html'})


def dealer_manager_add(request):
    a = DealerManager()
    if request.method == 'POST':
        form = DealerManagerForm(request.POST, instance = a)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            company = form.cleaned_data['company']
            description = form.cleaned_data['description']
            DealerManager(name=name, email=email, phone=phone, company=company, description=description).save()
            return HttpResponseRedirect('/dealer-manager/view/')
    else:
        form = DealerManagerForm(instance = a)
    #return render_to_response('dealer-manager.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer-manager.html'})


def dealer_manager_edit(request, id):
    a = DealerManager.objects.get(pk=id)
    if request.method == 'POST':
        form = DealerManagerForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dealer-manager/view/')
    else:
        form = DealerManagerForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer-manager.html'})

 
def dealer_manager_del(request, id):
    obj = DealerManager.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer-manager/view/')
 
 
def dealer_manager_list(request):
    list = DealerManager.objects.all()
    #return render_to_response('dealer-manager_list.html', {'dealer_managers': list.values_list()})
    return render_to_response('index.html', {'dealer_managers': list, 'weblink': 'dealer-manager_list.html'})


def dealer_payment_add(request):
    a = DealerPayment()
    if request.method == 'POST':
        form = DealerPaymentForm(request.POST, instance = a)
        if form.is_valid():
            dealer_invoice = form.cleaned_data['dealer_invoice']
            invoice_number = form.cleaned_data['invoice_number']
            date = form.cleaned_data['date']
            bank = form.cleaned_data['bank']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            letter = form.cleaned_data['letter']
            desc = form.cleaned_data['description']

            if currency == dealer_invoice.currency:
                if dealer_invoice.price <= price:
                     obj = DealerInvoice.objects.get(id=dealer_invoice.id)
                     obj.payment = True
                     obj.save()
            else:
                if dealer_invoice.currency.id == 3:
                    exchange_dealer = 1
                    d = dealer_invoice.price
                else:
                    exchange_dealer = Exchange.objects.get(date=datetime.date.today, currency=str(dealer_invoice.currency.id))
                    d = dealer_invoice.price * float(exchange_dealer.value)
                if currency.id == 3:
                    exchange_pay = 1
                    p = price
                else:
                    exchange_pay = Exchange.objects.get(date=datetime.date.today, currency=str(currency.id))
                    p = price * float(exchange_pay.value)
                if d <= p:
                     obj = DealerInvoice.objects.get(id=dealer_invoice.id)
                     obj.payment = True
                     #obj.save()
           
            DealerPayment(dealer_invoice=dealer_invoice, invoice_number=invoice_number, date=date, bank=bank, price=price, currency=currency, letter=letter, description=desc).save()
            return HttpResponseRedirect('/dealer/payment/view/')
    else:
        form = DealerPaymentForm(instance = a)
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer_payment.html'})

 
def dealer_payment_del(request, id):
    obj = DealerPayment.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer/payment/view/')
 
 
def dealer_payment_list(request):
    list = DealerPayment.objects.all()
    return render_to_response('index.html', {'dealer_payment': list, 'weblink': 'dealer_payment_list.html'})


def dealer_invoice_add(request):
    a = DealerInvoice(date=datetime.date.today())
    if request.method == 'POST':
        form = DealerInvoiceForm(request.POST, instance = a)
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
            DealerInvoice(origin_id=origin_id, date=date, company=company, manager=manager, price=price, currency=currency, file=file, received=received, description=description).save()
            return HttpResponseRedirect('/dealer/invoice/view/')
    else:
        form = DealerInvoiceForm(instance = a)
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer_invoice.html'})


def dealer_invoice_edit(request, id):
    a = DealerInvoice.objects.get(pk=id)
    if request.method == 'POST':
        form = DealerInvoiceForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            mmm = a.date.month
            yyy = a.date.year
            now = datetime.datetime.now()
            #m = now.month
            return HttpResponseRedirect('/dealer/invoice/year/'+str(yyy)+'/month/'+str(mmm)+'/view/')
    else:
        form = DealerInvoiceForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'dealer_invoice.html'})

 
def dealer_invoice_del(request, id):
    obj = DealerInvoice.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/dealer/invoice/view/')
 

 
def dealer_invoice_list(request, id=False, pay='all'):
    if id == False:
        list = DealerInvoice.objects.all()
    else:
        list = DealerInvoice.objects.filter(company=id)
        if pay == 'paid':
            list = DealerInvoice.objects.filter(company=id, payment=True)
        if pay == 'notpaid':
            list = DealerInvoice.objects.filter(company=id, payment=False)
        if pay == 'sending':
            list = DealerInvoice.objects.filter(company=id, received=False)
        if pay == 'all':
            list = DealerInvoice.objects.filter(company=id)   

    now = datetime.datetime.now()
    year=now.year
            
    exchange = Exchange.objects.filter(date=datetime.date.today)
    try:
        exchange_d = Exchange.objects.get(date=datetime.date.today, currency=2)
        exchange_e = Exchange.objects.get(date=datetime.date.today, currency=4)
        summ = 0
        summ_debt = 0
        for e in list: 
        #DealerInvoice.objects.all():
            if e.currency.id == 2:
                summ = summ + (float(e.price) * float(exchange_d.value))
                if e.payment != True:
                    summ_debt = summ_debt + (float(e.price) * float(exchange_d.value))
            if e.currency.id == 4:
                summ = summ + (float(e.price) * float(exchange_e.value))
                if e.payment != True:
                    summ_debt = summ_debt + (float(e.price) * float(exchange_e.value))
            if e.currency.id == 3:
                summ = summ + e.price
                if e.payment != True:
                    summ_debt = summ_debt + e.price
                
        
    except Exchange.DoesNotExist:
        now = datetime.date.today()
        html = "<html><body>Не має курсу валют. Введіть <a href=""/exchange/view/"" >курс валют на сьогодні</a> (%s) та спробуйте знову.</body></html>" % now
        return HttpResponse(html)
         
        exchange_d = 0
        exchange_e = 0
        
    return render_to_response('index.html', {'dealer_invoice': list, 'sel_company': id, 'sel_year': year, 'exchange': exchange, 'exchange_d': exchange_d, 'exchange_e': exchange_e, 'summ': summ, 'summ_debt': summ_debt, 'weblink': 'dealer_invoice_list.html'})


def dealer_invoice_list_month(request, year=False, month=False, pay='all'):
    if month == False:
        now = datetime.datetime.now()
        month=now.month
    if year == False:
        now = datetime.datetime.now()
        year=now.year
    list = None
    if pay == 'paid':
            list = DealerInvoice.objects.filter(date__year=year, payment=True)
    if pay == 'notpaid':
            list = DealerInvoice.objects.filter(date__year=year, payment=False)
    if pay == 'sending':
            list = DealerInvoice.objects.filter(date__year=year, received=False)
    if pay == 'all':
            list = DealerInvoice.objects.filter(date__year=year, date__month=month)                        
    #list = DealerInvoice.objects.filter(date__year=year, date__month=month, payment=)
    exchange = Exchange.objects.filter(date=datetime.date.today)
    try:
        exchange_d = Exchange.objects.get(date=datetime.date.today, currency=2)
        exchange_e = Exchange.objects.get(date=datetime.date.today, currency=4)
        summ = 0
        summ_debt = 0
        #DealerInvoice.objects.filter(date__year=year, date__month=month):
        for e in list:
            if e.currency.id == 2:
                summ = summ + (float(e.price) * float(exchange_d.value))
                if e.payment != True:
                    summ_debt = summ_debt + (float(e.price) * float(exchange_d.value))
            if e.currency.id == 4:
                summ = summ + (float(e.price) * float(exchange_e.value))
                if e.payment != True:
                    summ_debt = summ_debt + (float(e.price) * float(exchange_e.value))
            if e.currency.id == 3:
                summ = summ + e.price
                if e.payment != True:
                    summ_debt = summ_debt + e.price
                
        
    except Exchange.DoesNotExist:
        now = datetime.date.today()
        html = "<html><body>Не має курсу валют. Введіть <a href=""/exchange/view/"" >курс валют на сьогодні</a> (%s) та спробуйте знову.</body></html>" % now
        return HttpResponse(html)
         
        exchange_d = 0
        exchange_e = 0
    
    return render_to_response('index.html', {'dealer_invoice': list, 'exchange': exchange, 'exchange_d': exchange_d, 'exchange_e': exchange_e, 'summ': summ, 'summ_debt': summ_debt, 'sel_month':month, 'sel_year':year, 'weblink': 'dealer_invoice_list.html'})


def dealer_invoice_search(request):
    #query = request.GET.get('q', '')
    return render_to_response('index.html', {'weblink': 'dealer_invoice_search.html'})


def dealer_invoice_search_result(request):
    list = None
    if 'number' in request.GET and request.GET['number']:
        num = request.GET['number']
        list = DealerInvoice.objects.filter(origin_id__icontains = num)
    #list1 = DealerInvoice.objects.all()
    return render_to_response('index.html', {'invoice_list': list, 'weblink': 'dealer_invoice_list_search.html'})


#-------------- InvoiceComponentList -----------------------
def invoicecomponent_add(request, mid=None, cid=None):
    company_list = Manufacturer.objects.all()
    if cid<>None:
        #a = InvoiceComponentList(date=datetime.date.today(), price=0, count=1, currency=Currency.objects.get(id=2), invoice=DealerInvoice.objects.get(id=187), catalog=Catalog.objects.get(id=cid))        
        a = InvoiceComponentList(date=datetime.date.today(), price=0, count=1, currency=Currency.objects.get(id=2), invoice=DealerInvoice.objects.get(id=187), catalog=Catalog.objects.get(id=cid))
    else:    
        a = InvoiceComponentList(date=datetime.date.today(), price=0, count=1, currency=Currency.objects.get(id=2), invoice=DealerInvoice.objects.get(id=187))
    if request.method == 'POST':
        form = InvoiceComponentListForm(request.POST, instance = a, test1=mid, catalog_id=cid)
        if form.is_valid():
            invoice = form.cleaned_data['invoice']
            date = form.cleaned_data['date']
            catalog = form.cleaned_data['catalog']
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            InvoiceComponentList(date=date, invoice=invoice, catalog=catalog, price=price, currency=currency, count=count, description=description).save()
            cat = Catalog.objects.get(id = cid)
            cat.count = cat.count + count
            cat.save()
            #return HttpResponseRedirect('/invoice/list/10/view/')
            #list = InvoiceComponentList.objects.all().values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale').order_by('-id')[:10]
            #return render_to_response('index.html', {'componentlist': list, 'addurl': "/invoice/manufacture/"+str(mid)+"/add", 'weblink': 'invoicecomponent_list.html'})
            return HttpResponseRedirect('/invoice/list/10/view/')
    else:
        form = InvoiceComponentListForm(instance = a, test1=mid, catalog_id=cid)
    return render_to_response('index.html', {'form': form, 'weblink': 'invoicecomponent.html', 'company_list': company_list})


def invoicecomponent_list(request, mid=None, limit=0):
    company_list = Manufacturer.objects.all()    
    list = None
    id_list=[]
    zsum = 0
    zcount = 0
    
    if limit == 0:
        list = InvoiceComponentList.objects.all().values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale', 'catalog__count').annotate(sum_catalog=Sum('count')).order_by("catalog__type")        
    else:
        list = InvoiceComponentList.objects.filter(catalog__count__gt=0).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale', 'catalog__count').annotate(sum_catalog=Sum('count')).order_by("catalog__type")
        list = list[:limit]
        #list = list.order_by("catalog__manufacturer__name")
        #list = list.filter(catalog=90)                
#        list = InvoiceComponentList.objects.filter(catalog__count__lt=0).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale', 'catalog__count').annotate(sum_catalog=Sum('count')).order_by("-id")
#        list = InvoiceComponentList.objects.all().values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale', 'catalog__count').annotate(sum_catalog=Sum('count')).order_by("-id")

    for item in list:
        id_list.append(item['catalog'])
        item['balance']=item['sum_catalog']
        item['c_sale']=0

    new_list = []
    sale_list = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__price').annotate(sum_catalog=Sum('count'))        
    for element in list:
        for sale in sale_list:
            if element['catalog']==sale['catalog']:
                element['c_sale']=sale['sum_catalog']
                element['balance']=element['sum_catalog'] - element['c_sale']
            #else:
            #    element['balance']=element['sum_catalog'] 
        if element['balance']!=0:
            new_list.append(element)
            zsum = zsum + (element['balance'] * element['catalog__price'])
            zcount = zcount + element['balance']

# update count field in catalog table            
        #upd = Catalog.objects.get(pk = element['catalog'])
        #upd.count = element['balance'] 
        #upd.save()

        
    return render_to_response('index.html', {'company_list': company_list, 'componentlist': new_list, 'zsum':zsum, 'zcount':zcount, 'weblink': 'invoicecomponent_list.html'})
 

def invoicecomponent_list_by_manufacturer(request, mid=None, availability=False):
    company_list = Manufacturer.objects.all()
    list = None
    id_list=[]
    psum = 0
    zsum = 0
    scount = 0
    zcount = 0
    
    if availability == False:
        list = InvoiceComponentList.objects.filter(catalog__manufacturer__exact=mid).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale', 'catalog__count').annotate(sum_catalog=Sum('count')).order_by("catalog__type")
    else:
        list = InvoiceComponentList.objects.filter(catalog__manufacturer__exact=mid, catalog__count__gt=0).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale', 'catalog__count').annotate(sum_catalog=Sum('count')).order_by("catalog__type")

    for item in list:
        psum = psum + (item['catalog__price'] * item['sum_catalog'])
        scount = scount + item['sum_catalog']
        id_list.append(item['catalog'])
        item['balance']=item['sum_catalog']
#        list_sale = ClientInvoice.objects.filter(catalog__name__icontains=name).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__price').annotate(sum_catalog=Sum('count'))
#        list_sale = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__price').annotate(sum_catalog=Sum('count'))
    sale_list = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__price').annotate(sum_catalog=Sum('count'))        
    for element in list:
        element['c_sale']=0
        for sale in sale_list:
            if element['catalog']==sale['catalog']:
                element['c_sale']=sale['sum_catalog']
                element['balance']=element['sum_catalog'] - element['c_sale']
        zsum = zsum + ((element['sum_catalog'] - element['c_sale']) * element['catalog__price'])
        zcount = zcount + (element['sum_catalog'] - element['c_sale'])
#        return render_to_response('index.html', {'componentlist': list, 'salelist': list_sale, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'})

    if mid == None:
        company_name = ""
    else:
        company_name = company_list.get(id=mid)

    return render_to_response('index.html', {'company_list': company_list, 'company_name': company_name, 'company_id':mid, 'componentlist': list, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'}, context_instance=RequestContext(request, processors=[custom_proc]))

    
#===============================================================================
#    psum = 0
#    scount = 0
#    for item in list:
#        psum = psum + (item.catalog.price * item.count)
#        scount = scount + item.count
#    return render_to_response('index.html', {'company_list': company_list, 'componentlist': list, 'allpricesum':psum, 'countsum': scount, 'weblink': 'invoicecomponent_list.html'})
#===============================================================================


def invoicecomponent_list_by_category(request, cid=None, limit=0):
    category_list = Type.objects.filter(name_ukr__isnull=False).order_by('name_ukr')

    list = None
    id_list=[]
    psum = 0
    zsum = 0
    scount = 0
    zcount = 0
    
    if limit == 0:
        list = InvoiceComponentList.objects.filter(catalog__type__exact=cid).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale').annotate(sum_catalog=Sum('count')).order_by('catalog__manufacturer__name')
    else:
        list = InvoiceComponentList.objects.filter(catalog__type__exact=cid).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale').annotate(sum_catalog=Sum('count'))[:limit]
        
    for item in list:
        psum = psum + (item['catalog__price'] * item['sum_catalog'])
        scount = scount + item['sum_catalog']
        id_list.append(item['catalog'])
        item['balance']=item['sum_catalog']
#        list_sale = ClientInvoice.objects.filter(catalog__name__icontains=name).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__price').annotate(sum_catalog=Sum('count'))
#        list_sale = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__price').annotate(sum_catalog=Sum('count'))
    sale_list = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__price').annotate(sum_catalog=Sum('count'))        
    for element in list:
        element['c_sale']=0
        for sale in sale_list:
            if element['catalog']==sale['catalog']:
                element['c_sale']=sale['sum_catalog']
                element['balance']=element['sum_catalog'] - element['c_sale']
        zsum = zsum + ((element['sum_catalog'] - element['c_sale']) * element['catalog__price'])
        zcount = zcount + (element['sum_catalog'] - element['c_sale'])
#        return render_to_response('index.html', {'componentlist': list, 'salelist': list_sale, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'})

    if cid == None:
        cat_name = ""
    else:
        cat_name = category_list.get(id=cid)


    return render_to_response('index.html', {'category_list': category_list, 'category_name': cat_name, 'componentlist': list, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'}, context_instance=RequestContext(request, processors=[custom_proc]))


def invoicecomponent_manufacturer_html(request, mid):
    list = Catalog.objects.filter(manufacturer__id=mid, count__gt=0)
    zcount = 0
    for elem in list:
        zcount = zcount + elem.count
    
    if mid == None:
        company_name = ""
    else:
        company_name = Manufacturer.objects.get(id=mid)
        
    return render_to_response('index.html', {'componentlist': list, 'company_name': company_name, 'zcount': zcount, 'weblink': 'component_list_by_manufacturer_html.html'})


from django.db.models import F

def invoicecomponent_sum(request):
    list = InvoiceComponentList.objects.all().aggregate(price_sum=Sum('catalog__price'))
    psum = list['price_sum']
    scount = 0
#    for item in list:
#        psum = psum + (item.catalog.price * item.count)
#        scount = scount + item.count
    return render_to_response('index.html', {'allpricesum':psum, 'countsum': scount, 'weblink': 'invoicecomponent_report.html'})


def invoicecomponent_del(request, id):
    obj = InvoiceComponentList.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    cat = Catalog.objects.get(id = obj.catalog.id)
    cat.count = cat.count + obj.catalog.count
    cat.save()
    return HttpResponseRedirect('/invoice/list/10/view/')


def invoicecomponent_edit(request, id):
    a = InvoiceComponentList.objects.get(id=id)
    cid = a.catalog.id
    if request.method == 'POST':
        #form = InvoiceComponentListForm(request.POST, instance=a)
        form = InvoiceComponentListForm(request.POST, instance=a, catalog_id=cid)
        if form.is_valid():
            invoice = form.cleaned_data['invoice']
            date = form.cleaned_data['date']
            catalog = form.cleaned_data['catalog']
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            currency = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            form.save()
            cat = Catalog.objects.get(id = cid)
            cat.count = cat.count + count
            cat.save()
            return HttpResponseRedirect('/invoice/list/10/view/')
    else:
        form = InvoiceComponentListForm(instance=a, catalog_id=cid)
        #form = InvoiceComponentListForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'invoicecomponent.html'})


def invoice_search(request):
    return render_to_response('index.html', {'weblink': 'invoice_search.html'})


def invoice_search_result(request):
    list = None
    psum = 0
    zsum = 0
    scount = 0
    zcount = 0
    id_list = []
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
        #list = Catalog.objects.filter(name__icontains = name).order_by('manufacturer') 
        list = InvoiceComponentList.objects.filter(catalog__name__icontains=name).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale').annotate(sum_catalog=Sum('count'))
    elif  'id' in request.GET and request.GET['id']:
        id = request.GET['id']
        #list = InvoiceComponentList.objects.filter(catalog__ids__icontains=id)
        list = InvoiceComponentList.objects.filter(catalog__ids__icontains=id).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale').annotate(sum_catalog=Sum('count'))
        #list = Catalog.objects.filter(ids__icontains = id).order_by('manufacturer')

    for item in list:
        psum = psum + (item['catalog__price'] * item['sum_catalog'])
        scount = scount + item['sum_catalog']
        id_list.append(item['catalog'])
#        list_sale = ClientInvoice.objects.filter(catalog__name__icontains=name).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__price').annotate(sum_catalog=Sum('count'))
#        list_sale = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__price').annotate(sum_catalog=Sum('count'))
    sale_list = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__price').annotate(sum_catalog=Sum('count'))        
    for element in list:
        element['c_sale']=0
        for sale in sale_list:
            if element['catalog']==sale['catalog']:
                element['c_sale']=sale['sum_catalog']
        zsum = zsum + ((element['sum_catalog'] - element['c_sale']) * element['catalog__price'])
        zcount = zcount + (element['sum_catalog'] - element['c_sale'])
#        return render_to_response('index.html', {'componentlist': list, 'salelist': list_sale, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'})

    return render_to_response('index.html', {'componentlist': list, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'})
    #return render_to_response('index.html', {'componentlist': list, 'allpricesum':psum, 'countsum': scount, 'weblink': 'invoicecomponent_list.html'})        


def invoice_report(request):
    #list = InvoiceComponentList.objects.all().order_by('-id')[:10]
    
    query = '''select accounting_invoicecomponentlist.id, count(*) as ccount, accounting_invoicecomponentlist.invoice_id as invoice, sum(accounting_invoicecomponentlist.price*accounting_invoicecomponentlist.count) as suma, accounting_dealerinvoice.origin_id
    from accounting_invoicecomponentlist left join accounting_dealerinvoice on accounting_dealerinvoice.id=invoice_id  
    group by accounting_invoicecomponentlist.invoice_id;'''
    company_list = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        company_list = dictfetchall(cursor)
        
    except TypeError:
        res = "Помилка"
    
    return render_to_response('index.html', {'list': list, 'company_list':company_list, 'weblink': 'invoice_component_report.html'})


def invoice_id_list(request, id=None, limit=0):
#    query = "select id, count(*) as ccount, invoice_id as invoice, sum(price*count) as suma from accounting_invoicecomponentlist group by invoice_id;"
    query = '''select accounting_invoicecomponentlist.id, count(*) as ccount, accounting_invoicecomponentlist.invoice_id as invoice, sum(accounting_invoicecomponentlist.price*accounting_invoicecomponentlist.count) as suma, accounting_dealerinvoice.origin_id
    from accounting_invoicecomponentlist left join accounting_dealerinvoice on accounting_dealerinvoice.id=invoice_id  
    group by accounting_invoicecomponentlist.invoice_id;'''
    
    company_list = None
#===============================================================================
#    try:
#        cursor = connection.cursor()
#        cursor.execute(query)
#        company_list = dictfetchall(cursor)
#        
#    except TypeError:
#        res = "Помилка"
#===============================================================================

    list = None
    if limit == 0:
        list = InvoiceComponentList.objects.filter(invoice=id).order_by('-id')
    else:
        list = InvoiceComponentList.objects.filter(invoice=id).order_by('-id')[:limit]
    psum = 0
    optsum = 0
    scount = 0
    for item in list:
        psum = psum + (item.catalog.price * item.count)
        optsum = optsum + (item.count * item.price)
        scount = scount + item.count
    dinvoice = DealerInvoice.objects.get(id=id)    
    
    #return render_to_response('index.html', {'list': list, 'dinvoice':dinvoice, 'company_list':company_list, 'allpricesum':psum, 'alloptsum':optsum, 'countsum': scount, 'weblink': 'invoice_component_report.html'})
    return render_to_response('index.html', {'list': list, 'dinvoice':dinvoice, 'allpricesum':psum, 'alloptsum':optsum, 'countsum': scount, 'weblink': 'invoice_component_report.html'})


def invoice_cat_id_list(request, cid=None, limit=0):
    list = InvoiceComponentList.objects.filter(catalog=cid).order_by('-id')
    psum = 0
    scount = 0
    for item in list:
        psum = psum + (item.catalog.price * item.count)
        scount = scount + item.count
        
    return render_to_response('index.html', {'list': list, 'allpricesum':psum, 'countsum': scount, 'weblink': 'invoice_component_report.html'})


# --------------- Classification ---------

def category_list(request):
    list = Type.objects.all()
    #return render_to_response('category_list.html', {'categories': list.values_list()})
    return render_to_response('index.html', {'categories': list, 'weblink': 'category_list.html'})

def category_add(request):
    a = Type()
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance = a)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            name_ukr = form.cleaned_data['name_ukr']
            description_ukr = form.cleaned_data['description_ukr']

            Type(name=name, description=description, name_ukr=name_ukr, description_ukr=description_ukr).save()
            return HttpResponseRedirect('/category/view/')
    else:
        form = CategoryForm(instance = a)
    #return render_to_response('category.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'category.html'})

def category_edit(request, id):
    a = Type.objects.get(pk=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/category/view/')
    else:
        form = CategoryForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'category.html', 'text': 'Обмін валют (редагування)'})

def category_del(request, id):
    obj = Type.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/category/view/')    

# -------------- Currency and operations ----------------------
def curency_add(request):
    a = Currency()
    if request.method == 'POST':
        form = CurencyForm(request.POST, instance = a)
        if form.is_valid():
            ids = form.cleaned_data['ids']
            ids_char = form.cleaned_data['ids_char']
            name = form.cleaned_data['name']
            country_id = form.cleaned_data['country_id']
            Currency(ids=ids, ids_char=ids_char, name=name, country_id=country_id).save()
            return HttpResponseRedirect('/curency/view/')
    else:
        form = CurencyForm(instance = a)
    #return render_to_response('curency.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'curency.html'})


def curency_list(request):
    list = Currency.objects.all()
    #return render_to_response('curency_list.html', {'currency': list.values()})
    return render_to_response('index.html', {'currency': list, 'weblink': 'curency_list.html'})


def curency_del(request, id):
    obj = Currency.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/curency/view/')


def exchange_add(request):
    a = Exchange(date = datetime.datetime.now())
    if request.method == 'POST':
        form = ExchangeForm(request.POST, instance = a)
        if form.is_valid():
            date = form.cleaned_data['date']
            currency = form.cleaned_data['currency']
            value = form.cleaned_data['value']
            Exchange(date=date, currency=currency, value=value).save()
            return HttpResponseRedirect('/exchange/view/')
    else:
        form = ExchangeForm(instance = a)
    #return render_to_response('exchange.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'exchange.html'})


def exchange_list(request):
    curdate = datetime.datetime.now()
    list = Exchange.objects.filter(date__month=curdate.month)
    #return render_to_response('exchange_list.html', {'exchange': list.values()})
    return render_to_response('index.html', {'exchange': list, 'weblink': 'exchange_list.html'})


def exchange_edit(request, id):
    a = Exchange.objects.get(pk=id)
    if request.method == 'POST':
        form = ExchangeForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/exchange/view/')
    else:
        form = ExchangeForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'exchange.html', 'text': 'Обмін валют (редагування)'})


def exchange_del(request, id):
    obj = Exchange.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/exchange/view/')



# -------- Catalog ---------------- 

def manufacturer_add(request):
    a = Manufacturer()
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES, instance=a)
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
        form = ManufacturerForm(instance=a)
    #return render_to_response('manufacturer.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'manufacturer.html'})


def manufacturer_edit(request, id):
    a = Manufacturer.objects.get(pk=id)
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES, instance=a)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            www = form.cleaned_data.get('www')
            country = form.cleaned_data.get('country')
            logo = form.cleaned_data.get('logo')
            upload_path = processUploadedImage(logo, 'manufecturer/') 
            #a = Manufacturer(name=name, description=description, www=www, logo=upload_path, country=country)
            #a.save()
            form.save()
            return HttpResponseRedirect('/manufacturer/view/')
    else:
        form = ManufacturerForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'manufacturer.html', 'text': 'Виробник (редагування)'})


def manufaturer_list(request):
    list = Manufacturer.objects.all()
    #return render_to_response('manufacturer_list.html', {'manufactures': list.values_list()})
    return render_to_response('index.html', {'manufactures': list, 'weblink': 'manufacturer_list.html'})


def manufacturer_delete(request, id):
    obj = Manufacturer.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/manufacturer/view/')



def catalog_add(request):
    upload_path = ''
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
            price = form.cleaned_data['price']
            count = form.cleaned_data['count']
            length = form.cleaned_data['length']
            currency = form.cleaned_data['currency']
            description = form.cleaned_data['description']
            if photo != None:               
                upload_path = processUploadedImage(photo, 'catalog/') 
            Catalog(ids=ids, name=name, manufacturer=manufacturer, type=type, size=size, weight=weight, year=year, sale=sale, sale_to=sale_to, color=color, description=description, photo=upload_path, country=country, price=price, currency=currency, count=count, length=length).save()
            #return HttpResponseRedirect('/catalog/view/')
            return HttpResponseRedirect('/catalog/manufacture/' + str(manufacturer.id) + '/view/5')
    else:
        form = CatalogForm()
    #return render_to_response('catalog.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'catalog.html'})


def catalog_edit(request, id):
    a = Catalog.objects.get(pk=id)
    url1=request.META['HTTP_REFERER']
    if request.method == 'POST':
        form = CatalogForm(request.POST, instance=a)
        if form.is_valid():
            manufacturer = form.cleaned_data['manufacturer']
            type = form.cleaned_data['type']
            form.save()
            #return HttpResponseRedirect('/catalog/manufacture/' + str(manufacturer.id) + '/view/5')
            return HttpResponseRedirect('/catalog/manufacture/' + str(manufacturer.id) + '/type/'+str(type.id)+'/view')
            #return HttpResponseRedirect(str(url1))
    else:
        form = CatalogForm(instance=a)
    #url=request.META['HTTP_REFERER']
    return render_to_response('index.html', {'form': form, 'myurl':url1, 'weblink': 'catalog.html'})


def catalog_list(request, id=None):
    list = None
    if id==None:
        list = Catalog.objects.all().order_by("-id")[:10]
    else:
        list = Catalog.objects.filter(id=id)
    #return render_to_response('catalog_list.html', {'catalog': list.values_list()})
    return render_to_response('index.html', {'catalog': list, 'weblink': 'catalog_list.html'})


def catalog_discount_list(request):
    list = Catalog.objects.filter(sale__gt=0)[:100]
    return render_to_response('index.html', {'catalog': list, 'weblink': 'catalog_list.html'})


def catalog_manufacture_list(request, id=None):
    company_list = Manufacturer.objects.all()
    #list = Catalog.objects.filter(manufacturer=id)[:10]
    if id<>None:
        list = Catalog.objects.filter(manufacturer=id).order_by("-id")
    else:
        list = Catalog.objects.filter(manufacturer=id).order_by("-id")
    #return render_to_response('catalog_list.html', {'catalog': list.values_list()})
    return render_to_response('index.html', {'catalog': list, 'company_list': company_list, 'view': True, 'weblink': 'catalog_list.html'})


def catalog_part_list(request, id, num=5):
    list = Catalog.objects.filter(manufacturer=id).order_by("-id")[:num]
    #return render_to_response('catalog_list.html', {'catalog': list.values_list()})
    return render_to_response('index.html', {'catalog': list, 'weblink': 'catalog_list.html'})


def catalog_manu_type_list(request, id, tid):
    list = Catalog.objects.filter(manufacturer=id, type=tid).order_by("-id")
    #return render_to_response('catalog_list.html', {'catalog': list.values_list()})
    return render_to_response('index.html', {'catalog': list, 'weblink': 'catalog_list.html'})


def catalog_type_list(request, id):
    list = Catalog.objects.filter(type=id)
    #return render_to_response('catalog_list.html', {'catalog': list.values_list()})
    return render_to_response('index.html', {'catalog': list, 'weblink': 'catalog_list.html'})


def catalog_delete(request, id):
    obj = Catalog.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/catalog/search/')


def catalog_search(request):
    #query = request.GET.get('q', '')
    return render_to_response('index.html', {'weblink': 'catalog_search.html'})


def catalog_search_id(request):
    return render_to_response('index.html', {'weblink': 'catalog_search_id.html'})


def catalog_search_result(request):
    list = None
    print_url = None
    if 'name' in request.GET and request.GET['name']:
        name = request.GET['name']
        list = Catalog.objects.filter(name__icontains = name).order_by('manufacturer')
        print_url = "/shop/price/bysearch_name/"+name+"/view/"
    elif  'id' in request.GET and request.GET['id']:
        id = request.GET['id']
        list = Catalog.objects.filter(ids__icontains = id).order_by('manufacturer')
        print_url = "/shop/price/bysearch_id/"+id+"/view/"
    return render_to_response('index.html', {'catalog': list, 'url':print_url, 'weblink': 'catalog_list.html'})


def catalog_tresult(request):
        #list = Catalog.objects.filter(name__icontains = "Камера", type=84).order_by('manufacturer')
        list = Catalog.objects.filter(name__icontains = "Камера").order_by('manufacturer')
        list.update(type=51)    
        return render_to_response('index.html', {'catalog': list, 'weblink': 'catalog_list.html'})
        


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
 
            a = Client(name=name, forumname=forumname, country=country, city=city, email=email, phone=phone, sale=sale, summ=summ, description=description)
            a.save()
            #return HttpResponseRedirect('/client/view/')
            return HttpResponseRedirect('/client/result/search/?id=' + str(a.id))
    else:
        form = ClientForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'client.html'})


def client_edit(request, id):
    a = Client.objects.get(pk=id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
#===============================================================================
#            client = form.cleaned_data['client']
#            date = form.cleaned_data['date']
#            work_type = form.cleaned_data['work_type']
#            price = form.cleaned_data['price']
#            description = form.cleaned_data['description']
#            WorkShop(id=id, client=client, date=date, work_type=work_type, price=price, description=description).save()
#===============================================================================
            return HttpResponseRedirect('/client/view/')
    else:
        form = ClientForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'client.html'})


def client_balance_list(request):
    query = '''select accounting_client.id as id, accounting_client.name as name, sum(accounting_clientdebts.price) as sum_deb 
            from accounting_client 
            left join accounting_clientdebts on accounting_clientdebts.client_id=accounting_client.id 
            group by accounting_client.id order by accounting_client.id;
            '''
    query1 = '''select accounting_client.id as id, sum(accounting_clientcredits.price) as sum_cred 
            from accounting_client 
            left join accounting_clientcredits on accounting_clientcredits.client_id=accounting_client.id 
            group by accounting_client.id order by accounting_client.id;
            '''
            
#===============================================================================
#    query = '''select accounting_client.id as id, accounting_client.name as name, sum(accounting_clientcredits.price) as sum_cred, sum(accounting_clientdebts.price) as sum_deb    
#            from accounting_client left join accounting_clientcredits on accounting_client.id=accounting_clientcredits.client_id 
#            left join accounting_clientdebts on  accounting_client.id=accounting_clientdebts.client_id 
#            group by accounting_clientcredits.client_id, accounting_clientdebts.client_id;
#            '''
#                
#===============================================================================
            
    list = None
    list1 = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        list = dictfetchall(cursor)
        cursor1 = connection.cursor()
        cursor1.execute(query1)
        list1 = cursor1.fetchall()
        #list = cursor.execute(sql1, )   
        
    except TypeError:
        res = "Помилка"


    for item in list1:
        for key in list:
            if item[0]==key['id']:
                key['sum_cred']=item[1]
                try:
                    key['sum_cred'] = int(key['sum_cred'])
                except TypeError:
                    key['sum_cred'] = 0  # or whatever you want to do
                try:
                    key['sum_deb'] = int(key['sum_deb'])
                except TypeError:
                    key['sum_deb'] = 0
                key['minus']=key['sum_cred']-key['sum_deb']
            #item[1]
    s_debt = 0
    s_cred = 0
    for key1 in list[:]:
        s_debt+=key1['sum_deb']
        s_cred+=key1['sum_cred']
        if (key1['sum_deb']==False) & (key1['sum_cred']==False):
            #key1['minus']=9999
            list.remove(key1)
            
    #list = Bicycle_Sale.objects.all().order_by('date')
    return render_to_response('index.html', {'clients': list, 'sum_debt':s_debt, 'sum_cred':s_cred, 'weblink': 'client_balance_list.html'})
            

def client_list(request):
    list = Client.objects.all()
    paginator = Paginator(list, 25)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    
    return render_to_response('index.html', {'clients': contacts, 'weblink': 'client_list.html'})


def client_delete(request, id):
    obj = Client.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/client/view/')


def client_data(request, id):
    obj = Client.objects.get(id=id)
    #return render_to_response('bicycle_list.html', {'bicycles': list.values_list()})
    return render_to_response('index.html', {'client': obj, 'weblink': 'client_data.html'})


def clientdebts_add(request, id=None):
    if request.method == 'POST':
        form = ClientDebtsForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            ClientDebts(client=client, date=date, price=price, description=description).save()
            
            update_client = Client.objects.get(id=client.id)
            update_client.summ = update_client.summ + price 
            update_client.save()
            
            if id != None:
                return HttpResponseRedirect('/client/result/search/?id='+str(id))
            else:
                return HttpResponseRedirect('/clientdebts/view/')
    else:
        if id != None:
            form = ClientDebtsForm(initial={'client': id, 'date': now, })
        else:
            form = ClientDebtsForm()
    #return render_to_response('clientdebts.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'clientdebts.html'})


def clientdebts_edit(request, id):
    a = ClientDebts.objects.get(pk=id)
    if request.method == 'POST':
        form = ClientDebtsForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
#===============================================================================
#            client = form.cleaned_data['client']
#            date = form.cleaned_data['date']
#            work_type = form.cleaned_data['work_type']
#            price = form.cleaned_data['price']
#            description = form.cleaned_data['description']
#            WorkShop(id=id, client=client, date=date, work_type=work_type, price=price, description=description).save()
#===============================================================================
            return HttpResponseRedirect('/clientdebts/view/')
    else:
        form = ClientDebtsForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'client.html'})


#BORG
def clientdebts_list(request):
    #list = ClientDebts.objects.select_related().all()
    list = ClientDebts.objects.all().order_by("-id")
    
    paginator = Paginator(list, 50)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        debts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        debts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        debts = paginator.page(paginator.num_pages)
    
    return render_to_response('index.html', {'clients': debts, 'weblink': 'clientdebts_list.html'})


def clientdebts_delete(request, id):
    obj = ClientDebts.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/clientdebts/view/')


def clientcredits_add(request, id=None):
    if request.method == 'POST':
        form = ClientCreditsForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            ClientCredits(client=client, date=date, price=price, description=description).save()
            if id != None:
                return HttpResponseRedirect('/client/result/search/?id='+str(id))
            else:
                return HttpResponseRedirect('/clientcredits/view/')
            
    else:
        if id != None:
            cred = ClientCredits.objects.filter(client=id).aggregate(Sum('price'))
            deb = ClientDebts.objects.filter(client=id).aggregate(Sum('price'))
            #values('price').annotate(sum_deb=Sum('price'))
            if cred['price__sum'] == None:
                cred['price__sum'] = 0
            if deb['price__sum'] == None:
                deb['price__sum'] = 0
            borg = deb['price__sum'] - cred['price__sum']
            if borg <= 0:
                borg = 0
            form = ClientCreditsForm(initial={'client': id, 'date': now, 'price': borg, 'description': "Закриття боргу "})
        else:
            form = ClientCreditsForm()
        #form = ClientCreditsForm()
    #return render_to_response('clientcredits.html', {'form': form})
    return render_to_response('index.html', {'form': form, 'weblink': 'clientcredits.html'})


def clientcredits_list(request):
    list = ClientCredits.objects.all().order_by("-id")
    
    paginator = Paginator(list, 50)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        credits = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        credits = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        credits = paginator.page(paginator.num_pages)
    
    return render_to_response('index.html', {'clients': credits, 'weblink': 'clientcredits_list.html'})

def clientcredits_edit(request, id):
    a = ClientCredits.objects.get(pk=id)
    if request.method == 'POST':
        form = ClientCreditsForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/clientcredits/view/')
    else:
        form = ClientCreditsForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'clientcredits.html'})


def clientcredits_delete(request, id):
    obj = ClientCredits.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/clientcredits/view/')


def client_invoice(request, cid=None):
    cat = Catalog.objects.get(id = cid)
    a = ClientInvoice(date=datetime.date.today(), price=cat.price, sum=Catalog.objects.get(id = cid).price, sale=int(Catalog.objects.get(id = cid).sale), pay=0, count=1, currency=Currency.objects.get(id=3), catalog=Catalog.objects.get(id = cid))
    if request.method == 'POST':
        form = ClientInvoiceForm(request.POST, instance = a, catalog_id=cid)
        if form.is_valid():
            client = form.cleaned_data['client']
            catalog = form.cleaned_data['catalog']
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            sum = form.cleaned_data['sum']
            currency = form.cleaned_data['currency']
            sale = form.cleaned_data['sale']
            pay = form.cleaned_data['pay']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']
            ClientInvoice(client=client, catalog=catalog, count=count, sum=sum, price=price, currency=currency, sale=sale, pay=pay, date=date, description=description).save()
            cat.count = cat.count - count
            cat.save()
            #WorkGroup(name=name, description=description).save()
            return HttpResponseRedirect('/client/invoice/view/')
    else:
        form = ClientInvoiceForm(instance = a, catalog_id=cid)
    return render_to_response('index.html', {'form': form, 'weblink': 'clientinvoice.html'})


def client_invoice_edit(request, id):
    a = ClientInvoice.objects.get(id=id)
    cat_id = a.catalog.id
    if request.method == 'POST':
        form = ClientInvoiceForm(request.POST, instance = a, catalog_id = cat_id)
        if form.is_valid():
            client = form.cleaned_data['client']
            catalog = form.cleaned_data['catalog']
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            sum = form.cleaned_data['sum']
            currency = form.cleaned_data['currency']
            sale = form.cleaned_data['sale']
            pay = form.cleaned_data['pay']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']
            ClientInvoice(id=id, client=client, catalog=catalog, count=count, sum=sum, price=price, currency=currency, sale=sale, pay=pay, date=date, description=description).save()
            return HttpResponseRedirect('/client/invoice/view/')
    else:
        form = ClientInvoiceForm(instance = a, catalog_id = cat_id)
    return render_to_response('index.html', {'form': form, 'weblink': 'clientinvoice.html'})


def client_invoice_view(request, month=None, year=None, day=None, id=None):
    
    if year == None:
        year = datetime.datetime.now().year
    if month == None:
        month = datetime.datetime.now().month

    if day == None:
        day = datetime.datetime.now().day
        list = ClientInvoice.objects.filter(date__year=year, date__month=month, date__day=day).order_by("-date", "-id")
    else:
        if day == 'all':
            list = ClientInvoice.objects.filter(date__year=year, date__month=month).order_by("-date", "-id")
        else:
            list = ClientInvoice.objects.filter(date__year=year, date__month=month, date__day=day).order_by("-date", "-id")
            
    psum = 0
    scount = 0
    for item in list:
        psum = psum + item.sum
        scount = scount + item.count
    days = xrange(1, calendar.monthrange(int(year), int(month))[1]+1)
    
    paginator = Paginator(list, 15)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        cinvoices = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        cinvoices = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        cinvoices = paginator.page(paginator.num_pages)
            
    return render_to_response('index.html', {'sel_year':year, 'sel_month':month, 'month_days':days, 'buycomponents': cinvoices, 'sumall':psum, 'countall':scount, 'weblink': 'clientinvoice_list.html', 'view': True})


def client_invoice_id(request, id):
    list = ClientInvoice.objects.filter(catalog__id=id).order_by("-date", "-id")
    psum = 0
    scount = 0
    for item in list:
        psum = psum + item.sum
        scount = scount + item.count
    
    paginator = Paginator(list, 15)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        cinvoices = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        cinvoices = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        cinvoices = paginator.page(paginator.num_pages)
    
    return render_to_response('index.html', {'buycomponents': cinvoices, 'sumall':psum, 'countall':scount, 'weblink': 'clientinvoice_list.html'})


def client_invoice_sale_report(request):
    query = "SELECT EXTRACT(year FROM date) as year, EXTRACT(month from date) as month, MONTHNAME(date) as month_name, COUNT(*) as bike_count, sum(price) as s_price FROM accounting_clientinvoice GROUP BY year,month;"
    #sql2 = "SELECT sum(price) FROM accounting_clientdebts WHERE client_id = %s;"
    #user = id;
    list = None
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        list = dictfetchall(cursor)
        #list = cursor.execute(sql1, )   
        
    except TypeError:
        res = "Помилка"
        
    sum = 0
    bike_sum = 0
    for month in list:
         sum = sum + month['s_price']
         bike_sum = bike_sum + month['bike_count']

    #list = Bicycle_Sale.objects.all().order_by('date')
    return render_to_response('index.html', {'bicycles': list, 'all_sum': sum, 'bike_sum': bike_sum, 'weblink': 'clientinvoice_sale_report.html'})



def client_invoice_delete(request, id):
    obj = ClientInvoice.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    cat = Catalog.objects.get(id = obj.catalog.id)
    cat.count = cat.count + obj.count
    cat.save()
    return HttpResponseRedirect('/client/invoice/view/')


def client_search(request):
    #query = request.GET.get('q', '')
    return render_to_response('index.html', {'weblink': 'client_search.html'})


from django.db.models import Q
def client_search_result(request):
    username = request.GET['name']
    #clients = Client.objects.filter(name__icontains=username)
    clients = Client.objects.filter(Q(name__icontains=username) | Q(forumname__icontains=username))
    paginator = Paginator(clients, 25)
    page = request.GET.get('page')
    if page == None:
        page = 1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    
    return render_to_response('index.html', {'clients':contacts, 'weblink': 'client_list.html'})


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
        res = "Такого клієнта не існує, або в нього не має заборгованостей"
    
    try:
        client_name = Client.objects.values('name', 'forumname', 'id').get(id=user)
    except ObjectDoesNotExist:
        client_name = ""
    
    credit_list = ClientCredits.objects.filter(client=user)
    debt_list = ClientDebts.objects.filter(client=user)
    
    client_invoice = ClientInvoice.objects.filter(client=user).order_by("-date", "-id")
    client_invoice_sum = 0
    for a in client_invoice:
        client_invoice_sum = client_invoice_sum + a.sum

    client_workshop_sum = 0
    client_workshop = WorkShop.objects.filter(client=user).order_by("-date")
    for a in client_workshop:
        client_workshop_sum = client_workshop_sum + a.price
            
    #list_debt = ClientDebts.objects.filter(client='2').values("client", "price").select_related('client')
    #list_debt = ClientDebts.objects.filter(client='2').select_related('client')
    #list_debt = ClientDebts.objects.filter(client='2').annotate(Sum("price"))
    #return render_to_response('index.html', {'clients': list_credit.values_list(), 'weblink': 'client_result.html'})
    #return render_to_response('index.html', {'clients': list_debt.values_list(), 'weblink': 'client_result.html'})
    return render_to_response('index.html', {'clients': res, 'invoice': client_invoice, 'client_invoice_sum': client_invoice_sum, 'workshop': client_workshop, 'client_workshop_sum': client_workshop_sum, 'weblink': 'client_result.html', 'debt_list': debt_list, 'credit_list': credit_list, 'client_name': client_name})


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


def workgroup_edit(request, id):
    a = WorkGroup.objects.get(pk=id)
    if request.method == 'POST':
        form = WorkGroupForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/workgroup/view/')
    else:
        form = WorkGroupForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'workgroup.html'})


def workgroup_list(request, id=None):
    list = WorkGroup.objects.all()
    return render_to_response('index.html', {'workgroups': list, 'weblink': 'workgroup_list.html'})


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


def worktype_edit(request, id):
    a = WorkType.objects.get(pk=id)
    if request.method == 'POST':
        form = WorkTypeForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/worktype/view/')
    else:
        form = WorkTypeForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'worktype.html'})


def worktype_list(request):
    list = WorkType.objects.all()
    return render_to_response('index.html', {'worktypes': list, 'weblink': 'worktype_list.html'})


def worktype_list(request, id=None):
    list = None
    if id != None:
        list = WorkType.objects.filter(work_group=id)
    else:
        list = WorkType.objects.all()
    
    return render_to_response('index.html', {'worktypes': list, 'weblink': 'worktype_list.html'})



def workgroup_list(request, id=None):
    list = None
    if id != None:
        list = WorkType.objects.filter(worktype=id)
    else:
        list = WorkGroup.objects.all()
    
    return render_to_response('index.html', {'workgroups': list, 'weblink': 'workgroup_list.html'})



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


def workstatus_edit(request, id):
    a = WorkStatus.objects.get(pk=id)
    if request.method == 'POST':
        form = WorkStatusForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/workstatus/view/')
    else:
        form = WorkStatusForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'workstatus.html'})


def workstatus_list(request):
    list = WorkStatus.objects.all()
    return render_to_response('index.html', {'workstatus': list.values_list(), 'weblink': 'workstatus_list.html'})


def workstatus_delete(request, id):
    obj = WorkStatus.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/workstatus/view/')


def workticket_add(request, id=None):
    client = None
    if id!=None:
        client = Client.objects.get(id=id)
    
    if request.method == 'POST':
        if client!=None:
            form = WorkTicketForm(request.POST, initial={'client': client.id, 'status': 1})
        else:
            form = WorkTicketForm(request.POST, initial={'status': 1})
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            end_date = form.cleaned_data['end_date']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            WorkTicket(client=client, date=date, end_date=end_date, status=status, description=description).save()
            return HttpResponseRedirect('/workticket/view/')
    else:
        #form = WorkTicketForm()

        if client != None:
            form = WorkTicketForm(initial={'client': client.id, 'status': 1})
        else:
            form = WorkTicketForm(initial={'date': datetime.datetime.today(), 'status': 1, 'end_date': datetime.datetime.now()+datetime.timedelta(3)})
        
        
    return render_to_response('index.html', {'form': form, 'weblink': 'workticket.html'})


def workticket_edit(request, id):
    a = WorkTicket.objects.get(pk=id)
    if request.method == 'POST':
        form = WorkTicketForm(request.POST, instance=a)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            end_date = form.cleaned_data['end_date']
            status = form.cleaned_data['status']
            description = form.cleaned_data['description']
            WorkTicket(id = id, client=client, date=date, end_date=end_date, status=status, description=description).save()
            return HttpResponseRedirect('/workticket/view/')
    else:
        form = WorkTicketForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'workticket.html'})


def workticket_list(request, year=None, month=None, all=False):
    cur_year = datetime.datetime.now().year
    if month != None:
        list = WorkTicket.objects.filter(date__year=cur_year, date__month=month)
    if (year == None) and (month == None):
        month = datetime.datetime.now().month
        list = WorkTicket.objects.filter(date__year=cur_year, date__month=month)
    if all == True:
        list = WorkTicket.objects.all()
    return render_to_response('index.html', {'workticket': list, 'sel_year':cur_year, 'weblink': 'workticket_list.html'})


def workticket_delete(request, id):
    obj = WorkTicket.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/workticket/view/')


def workshop_add(request, id=None):
    work = None
    if id != None:
        work = WorkType.objects.get(id=id)
        
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
        if work != None:
            form = WorkShopForm(initial={'work_type': work.id, 'price': work.price})
        else:        
            form = WorkShopForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'workshop.html'})


def workshop_edit(request, id):
    a = WorkShop.objects.get(pk=id)
    if request.method == 'POST':
        form = WorkShopForm(request.POST, instance=a)
        if form.is_valid():
            client = form.cleaned_data['client']
            date = form.cleaned_data['date']
            work_type = form.cleaned_data['work_type']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            WorkShop(id=id, client=client, date=date, work_type=work_type, price=price, description=description).save()
            return HttpResponseRedirect('/workshop/view/')
    else:
        form = WorkShopForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'workshop.html'})


def workshop_list(request, year=None, month=None, day=None):
    if year == None:
        year = datetime.datetime.now().year
    if month == None:
        month = datetime.datetime.now().month
    
    if day == None:
        day = datetime.datetime.now().day
        list = WorkShop.objects.filter(date__year=year, date__month=month, date__day=day).order_by("-date")
    else:
        if day == 'all':
            list = WorkShop.objects.filter(date__year=year, date__month=month).order_by("-date")
        else:
            list = WorkShop.objects.filter(date__year=year, date__month=month, date__day=day).order_by("-date")

    
#    list = WorkShop.objects.filter(date__year=year, date__month=month)
    sum = 0 
    for item in list:
        sum = sum + item.price
        
    days = xrange(1, calendar.monthrange(int(year), int(month))[1]+1)
    return render_to_response('index.html', {'workshop': list, 'summ':sum, 'sel_year':year, 'sel_month':month, 'month_days': days, 'weblink': 'workshop_list.html'})


def workshop_delete(request, id):
    obj = WorkShop.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/workshop/view/')


#------------- Shop operation --------------
def shopdailysales_add(request):
    if request.method == 'POST':
        form = ShopDailySalesForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            ShopDailySales(date=date, price=price, description=description).save()
            return HttpResponseRedirect('/shop/sale/view/')
    else:        
        form = ShopDailySalesForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'shop_daily_sales.html'})


def shopmonthlysales_view(request, year=now.year, month=now.month):
    if auth_group(request.user, 'admin') == False:
        return HttpResponseRedirect("/.")
    deb = ClientDebts.objects.filter(date__year=year, date__month=month).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)", 'day': "EXTRACT(day from date)"}).values('year', 'month', 'day').annotate(suma=Sum("price")).order_by()
    cred = ClientCredits.objects.filter(date__year=year, date__month=month).extra(select={'year': "EXTRACT(year FROM date)", 'month': "EXTRACT(month from date)", 'day': "EXTRACT(day from date)"}).values('year', 'month', 'day').annotate(suma=Sum("price")).order_by()
    sum_cred = 0
    sum_deb = 0
    
    for element in cred:
        element['cred']=0
        sum_cred = sum_cred + element['suma']
        for deb_element in deb:
            if (deb_element['year']==element['year']) and (deb_element['month']==element['month']) and (deb_element['day']==element['day']):
                element['deb']=deb_element['suma']
                sum_deb = sum_deb + deb_element['suma']
                #element['balance']=element['sum_catalog'] - element['c_sale']
            
    strdate = pytils_ua.dt.ru_strftime(u"%d %B %Y", now, inflected=True)
    date_month = pytils_ua.dt.ru_strftime(u"%B %Y", now, inflected=True)

    return render_to_response('index.html', {'sum_cred': sum_cred, 'sum_deb': sum_deb, 'Cdeb': deb, 'Ccred':cred, 'date': strdate, 'date_month': date_month, 'l_month': xrange(1,13), 'weblink': 'shop_monthly_sales_view.html'}, context_instance=RequestContext(request, processors=[custom_proc]))


def shopdailysales_view(request, year, month, day):
#    deb = ClientDebts.objects.values('date__year').annotate(suma=Sum("price"))
    deb = ClientDebts.objects.filter(date__year=year, date__month=month, date__day=day).order_by()
    cred = ClientCredits.objects.filter(date__year=year, date__month=month, date__day=day).order_by()

    deb_sum = 0
    cred_sum = 0
    for c in cred:
        cred_sum = cred_sum + c.price
    for d in deb:    
        deb_sum = deb_sum + d.price
    strdate = pytils_ua.dt.ru_strftime(u"%d %B %Y", now, inflected=True)
    return render_to_response('index.html', {'Cdeb': deb, 'Ccred':cred, 'date': strdate, 'd_sum': deb_sum, 'c_sum': cred_sum, 'weblink': 'shop_daily_sales_view.html'})


def shopdailysales_edit(request, id):
    a = ShopDailySales.objects.get(pk=id)
    if request.method == 'POST':
        form = ShopDailySalesForm(request.POST, instance=a)
        if form.is_valid():
            date = form.cleaned_data['date']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            ShopDailySales(id=id, date=date, price=price, description=description).save()
            return HttpResponseRedirect('/shop/sale/view/')
    else:
        form = ShopDailySalesForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'shop_monthly_sales.html'})


def shopdailysales_list(request, month=now.month):
    #list = ShopDailySales.objects.all()
    list = ShopDailySales.objects.filter(date__year=2011, date__month=month)
    sum = 0 
    for item in list:
        sum = sum + item.price
    return render_to_response('index.html', {'shopsales': list, 'summ':sum, 'weblink': 'shop_sales_list.html'})


def shopdailysales_delete(request, id):
    obj = ShopDailySales.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/shop/sale/view/')


#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import A4
#from reportlab.pdfbase import pdfmetrics
#from reportlab.pdfbase import ttfonts



def shop_price(request, mid, limit=0, pprint=False):
#    list = InvoiceComponentList.objects.filter(catalog__manufacturer__exact=id).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale', 'catalog__country__name').annotate(sum_catalog=Sum('count'))
    #list = InvoiceComponentList.objects.filter(manufacturer = id)
    company = Manufacturer.objects.get(id=mid)
    company_list = Manufacturer.objects.all()
    url = '/shop/price/company/'+mid+'/print/'
    
    list = None
    id_list=[]
    psum = 0
    zsum = 0
    scount = 0
    zcount = 0
    
    if limit == 0:
        list = InvoiceComponentList.objects.filter(catalog__manufacturer__exact=mid).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale').annotate(sum_catalog=Sum('count'))
    else:
        list = InvoiceComponentList.objects.filter(catalog__manufacturer__exact=mid).values('catalog', 'catalog__name', 'catalog__ids', 'catalog__manufacturer__name', 'catalog__price', 'catalog__sale').annotate(sum_catalog=Sum('count'))[:limit]

    for item in list:
        id_list.append(item['catalog'])
        item['balance']=item['sum_catalog']
        item['c_sale']=0
    new_list = []
    sale_list = ClientInvoice.objects.filter(catalog__in=id_list).values('catalog', 'catalog__price').annotate(sum_catalog=Sum('count'))        
    for element in list:
        #element['c_sale']=0
        
        for sale in sale_list:
            if element['catalog']==sale['catalog']:
                element['c_sale']=sale['sum_catalog']
                element['balance']=element['sum_catalog'] - element['c_sale']
            #else:
            #    element['balance']=element['sum_catalog'] 
        if element['balance']!=0:
            new_list.append(element)
       
#        return render_to_response('index.html', {'componentlist': list, 'salelist': list_sale, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'})
#    return render_to_response('index.html', {'company_list': company_list, 'company_name': company_name, 'componentlist': list, 'allpricesum':psum, 'zsum':zsum, 'zcount':zcount, 'countsum': scount, 'weblink': 'invoicecomponent_list_test.html'})
    if pprint:
        return render_to_response('price_list.html', {'catalog': new_list, 'company': company, 'company_list': company_list,})
    
    return render_to_response('index.html', {'catalog': new_list, 'company': company, 'company_list': company_list, 'weblink': 'price_list.html', 'view': True, 'link': url})


def shop_price_lastadd(request, id):
    url = '/shop/price/lastadded/'+id+'/print/'
    list = InvoiceComponentList.objects.all().order_by("-id")[:id]
    return render_to_response('index.html', {'catalog': list, 'weblink': 'price_list.html', 'view': True, 'link': url})    

    
def shop_price_lastadd_print(request, id):
    list = Catalog.objects.all().order_by("-id")[:id]
    return render_to_response('price_list.html', {'catalog': list})     


def shop_price_bysearch_id(request, id):
    url = '/shop/price/bysearch_id/'+id+'/print/'
    list = Catalog.objects.filter(ids__icontains=id).order_by("-id")
    return render_to_response('index.html', {'catalog': list, 'weblink': 'price_list.html', 'view': True, 'link': url})    

    
def shop_price_bysearch_id_print(request, id):
    list = Catalog.objects.filter(ids__icontains=id).order_by("-id")
    return render_to_response('price_list.html', {'catalog': list})    


def shop_price_bysearch_name(request, id):
    url = '/shop/price/bysearch_name/'+id+'/print/'
    list = Catalog.objects.filter(name__icontains=id).order_by("manufacturer","-id")
    return render_to_response('index.html', {'catalog': list, 'weblink': 'price_list.html', 'view': True, 'link': url})    

    
def shop_price_bysearch_name_print(request, id):
    list = Catalog.objects.filter(name__icontains=id).order_by("manufacturer","-id")
    return render_to_response('price_list.html', {'catalog': list})    


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
    return render_to_response('index.html', {'costtypes': list, 'weblink': 'costtype_list.html'})


def costtype_delete(request, id):
    obj = CostType.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/cost/type/view/')


def cost_add(request, id = None):
    cost = None
    if id != None: 
        cost = CostType(id=id)
        
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
        if cost != None:
            form = CostsForm(initial={'cost_type': cost.id})
        else:        
            form = CostsForm()
    return render_to_response('index.html', {'form': form, 'weblink': 'cost.html'})


def cost_edit(request, id):
    a = Costs.objects.get(pk=id)
    if request.method == 'POST':
        form = CostsForm(request.POST, instance=a)
        if form.is_valid():
            date = form.cleaned_data['date']
            cost_type = form.cleaned_data['cost_type']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            Costs(id=id, date=date, cost_type=cost_type, price=price, description=description).save()            

#            form.save()
            return HttpResponseRedirect('/cost/view/')
    else:
        form = CostsForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'cost.html'})


def cost_list(request):
    list = Costs.objects.all().order_by("-date")
    sum = 0
    for item in list:
        sum = sum + item.price
    return render_to_response('index.html', {'costs': list, 'summ': sum, 'weblink': 'cost_list.html'})


def cost_delete(request, id):
    obj = Costs.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/cost/view/')



from django.forms.models import inlineformset_factory, modelformset_factory
from django.forms.models import formset_factory


def formset_test(request, id):
    client = Client.objects.get(pk=id)
    
    ArticleFormSet = formset_factory(WorkShopForm, extra=1, can_delete=True)
    formset = ArticleFormSet(initial=[{'client': id, 'price': '1122'},])
    
    if request.method == 'POST':
        #formset = ArticleFormSet(request.POST, instance=client)
        formset = ArticleFormSet(request.POST)
        if formset.is_valid():
            #formset.save()
            for form in formset.forms:
                form.save()

            return HttpResponseRedirect('/workshop/view/')
    else:
        formset = ArticleFormSet(initial=[{'client': id, 'price': '1122'},{'client': id, 'price': '1122'},{'client': id, 'price': '1122'},])
        
    #return render_to_response("client_workshop.html", {"property_formset": formset, 'client': client})
    return render_to_response('index.html', {'property_formset': formset, 'client': client, 'weblink': 'client_workshop.html'})
    #return render_to_response("formset_test.html", {"formset": formset, 'client': client})


def inline_formset_test(request):
    #client = WorkShop.objects.get(pk=2)
    client = Client.objects.get(pk=2)
    WorkInlineFormSet = inlineformset_factory(Client, WorkShop, extra=1)
    
    if request.method == 'POST':
        #formset = ArticleFormSet(request.POST, instance=client)
        formset = WorkInlineFormSet(request.POST, instance=client)
        if formset.is_valid():
            #formset.save()
            for form in formset.forms:
                form.save()
            return HttpResponseRedirect('/workshop/view/')
    else:
        formset = WorkInlineFormSet(instance=client)
    return render_to_response("manage_client.html", {"property_formset": formset, 'client': client})
    #return render_to_response("formset_test.html", {"formset": formset, 'client': client})
    


def manage_works(request, author_id):
    client = WorkShop.objects.get(pk=author_id)
    MyFormSet = inlineformset_factory(Client, WorkShop, extra=1)
    if request.method == "POST":
        property_formset = MyFormSet(request.POST, request.FILES, instance=client)
        if property_formset.is_valid():
            for form in property_formset.forms:
                client = form.cleaned_data['client']
                #date = form.cleaned_data['date']
                work_type = form.cleaned_data['work_type']
                price = form.cleaned_data['price']
                description = form.cleaned_data['description']
                if form.id != None:
                    WorkShop(id=form.id, client=author_id, work_type=work_type, price=price, description=description).save()            
                else:
                    WorkShop(client=author_id, work_type=work_type, price=price, description=description).save()
#            property_formset.save()
#            property_formset = MyFormSet(instance=client)
            return HttpResponseRedirect('/workshop/view/')
            # Do something.
    else:
        property_formset = MyFormSet(instance=client)
    return render_to_response("formset_test.html", {"formset": property_formset,})        
#    return render_to_response("manage_client.html", {"property_formset": property_formset,})


def preorder_add(request):
    a = PreOrder(price=0, price_pay=0, date_pay=datetime.date.today(), date_delivery=datetime.date.today())
    if request.method == 'POST':
        form = PreOrderForm(request.POST, instance = a)
        if form.is_valid():
            date = form.cleaned_data['date']
            date_pay = form.cleaned_data['date_pay']
            date_delivery = form.cleaned_data['date_delivery']
            company = form.cleaned_data['company']
            manager = form.cleaned_data['manager']
            price = form.cleaned_data['price']
            price_pay = form.cleaned_data['price_pay']
            currency = form.cleaned_data['currency']
            file = form.cleaned_data['file']
            received = form.cleaned_data['received']
            description = form.cleaned_data['description']
            PreOrder(date=date, date_pay=date_pay, date_delivery=date_delivery, company=company, manager=manager, price=price, price_pay=price_pay, currency=currency, file=file, received=received, description=description).save()
            return HttpResponseRedirect('/preorder/view/')
    else:
        form = PreOrderForm(instance = a)
    return render_to_response('index.html', {'form': form, 'weblink': 'preorder.html'})


def preorder_list(request):
    list = PreOrder.objects.all()
    #return render_to_response('dealer_list.html', {'dealers': list.values_list()})
    return render_to_response('index.html', {'preorder1': list, 'weblink': 'preorder_list.html'})


def preorder_delete(request, id):
    obj = PreOrder.objects.get(id=id)
    del_logging(obj)
    obj.delete()
    return HttpResponseRedirect('/preorder/view/')


def preorder_edit(request, id):
    a = PreOrder.objects.get(pk=id)
    if request.method == 'POST':
        form = PreOrderForm(request.POST, instance=a)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/preorder/view/')
    else:
        form = PreOrderForm(instance=a)
    return render_to_response('index.html', {'form': form, 'weblink': 'preorder.html'})


def payform(request):
    checkbox_list = [x for x in request.POST if x.startswith('checkbox_')]
    list_id = []
    for id in checkbox_list:
        list_id.append( int(id.replace('checkbox_', '')) )
    ci = ClientInvoice.objects.filter(id__in=list_id)
    client = ci[0].client
    desc = ""
    sum = 0
    for inv in ci:
        if client!=inv.client:
            return render_to_response('index.html', {'weblink': 'error_manyclients.html'})
        client = inv.client
        #inv.pay = inv.sum
        desc = desc + inv.catalog.name + "; "
        sum = sum + inv.sum
        #inv.save() 
    
        
    #cdeb = ClientDebts(client=client, date=datetime.datetime.now(), price=sum, description=desc)
    #cdeb.save()
    url = '/client/result/search/?id=' + str(client.id)
    #.values('catalog', 'catalog__price', 'catalog__name', 'sum', 'client')
    return render_to_response('index.html', {'checkbox': list_id, 'invoice': ci, 'summ': sum, 'client': client, 'weblink': 'payform.html'})
    #return HttpResponseRedirect(url)


def client_payform(request):
    checkbox_list = [x for x in request.POST if x.startswith('checkbox_')]
    list_id = []
    for id in checkbox_list:
        list_id.append( int(id.replace('checkbox_', '')) )
    ci = ClientInvoice.objects.filter(id__in=list_id)
    client = ci[0].client
    desc = ""
    sum = 0
    for inv in ci:
        inv.pay = inv.sum
        desc = desc + inv.catalog.name + "; "
        sum = sum + inv.sum
        inv.save() 
    
    if 'pay' in request.POST and request.POST['pay']:
        pay = request.POST['pay']
        if float(request.POST['pay']) != 0:
            ccred = ClientCredits(client=client, date=datetime.datetime.now(), price=pay, description=desc)
            ccred.save()
        
    cdeb = ClientDebts(client=client, date=datetime.datetime.now(), price=sum, description=desc)
    cdeb.save()
    if client.id == 138:
        return HttpResponseRedirect('/client/invoice/view/')
    url = '/client/result/search/?id=' + str(client.id)
    return HttpResponseRedirect(url)


def ajax_search1(request):
    if request.method == 'GET':  
        GET = request.GET  
        if GET.has_key('q'):
            q = request.GET.get( 'q' )
            search = Country.objects.all()
            results = search.filter(name__contains = q)
            matches = ""
            for result in results:
                matches = matches + "%s\n" % (result.name)
            return HttpResponse(matches, mimetype="text/plain")


from django.utils import simplejson 
def ajax_search(request):
    results = []
    search = None
    if request.is_ajax():
        if request.method == 'GET':  
            GET = request.GET  
            if GET.has_key('term'):
                q = request.GET.get( 'term' )
                search = Client.objects.filter(name__icontains = q).values_list('name', flat=True)
                #results = search.filter(name__icontains = q).values_list('name', flat=True)
                #for i in search:
                #    results.append(i)
    else:
        message = "Error"
     
    return HttpResponse(simplejson.dumps(list(search)))

         

def sendemail(request):
#    send_mail('Rivelo shop', 'Here is the new message with you check.', 'rivelo@ymail.com', ['igor.panchuk@gmail.com'], fail_silently=False)
    send_mail('subj - Test rivelo check', 'Here is the new message with you check.', 'rivelo@ymail.com', ['igor.panchuk@gmail.com'],)
    #send_mail('subj - Test rivelo check', ‘message’, ‘from@mail.ru’, ‘rivelo@ymail.com’)        
    return render_to_response('index.html')


def xhr_test(request):
    if request.is_ajax():
        message = "Hello AJAX"
    else:
        message = "Hello"
    return HttpResponse(message, mimetype="text/plain")


from django.contrib import auth 

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    next = request.POST['next']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        auth.login(request, user)
        # Перенаправление на "правильную" страницу
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect("/.")            
    else:
        # Отображение страницы с ошибкой
        if next:
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect("/.")            


def logout(request):
    auth.logout(request)
    next_page = request.POST['next_page']
    # Перенаправление на страницу.
    if next_page:
        return HttpResponseRedirect(next_page)
    else:
        return HttpResponseRedirect("/.")


#    current_url = request.META.get('HTTP_REFERER')
#    stroka = "<h1>Acces denied</h1> <a href=" +  current_url + ">Prev Page</a>"
#    return HttpResponseNotFound(stroka)