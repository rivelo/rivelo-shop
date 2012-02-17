# -*- coding: utf-8 -*-
from django import forms
from models import Manufacturer, Country, Type, Bicycle_Type, Bicycle, Currency, FrameSize, Bicycle_Store, Catalog, Size, Bicycle_Sale, Bicycle_Order 
from models import DealerManager, DealerPayment, DealerInvoice, Dealer, Bank, ShopDailySales, PreOrder, InvoiceComponentList
from models import Client, ClientDebts, CostType, Costs, ClientCredits, WorkGroup, WorkType, WorkShop, WorkTicket, WorkStatus

import datetime

TOPIC_CHOICES = (
    ('general', 'General enquiry'),
    ('bug', 'Bug report'),
    ('suggestion', 'Suggestion'),
)

class SelectFromModel(forms.Field):
    widget = forms.Select()
    def __init__(self, objects, *args, **kwargs):
        self.objects = objects
        super(SelectFromModel, self).__init__(*args, **kwargs)
        self.loadChoices()
    def loadChoices(self):
        choices = ()
        for object in self.objects.order_by('id'):
            choices += ((object.id, object.name),)
        self.widget.choices = choices
    def clean(self, value):
        value = int(value)
        for cat_id, cat_title in self.widget.choices:
            if cat_id == value:
                return self.objects.get(pk=cat_id)
        raise forms.ValidationError(u'Error Country')


class ManufacturerForm(forms.ModelForm):
    name = forms.CharField()
    www = forms.URLField(initial='http://', help_text='url')
    country = forms.ModelChoiceField(queryset = Country.objects.all())
    logo = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea())


class CountryForm(forms.ModelForm):
    name = forms.CharField(label='Country name')


class BankForm(forms.ModelForm):
    name = forms.CharField(label='Bank name')


class CurencyForm(forms.ModelForm):
    ids = forms.CharField()
    ids_char = forms.CharField()
    name = forms.CharField()
    country = forms.ModelChoiceField(queryset = Country.objects.all())



class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object - %i" % obj.name


class ExchangeForm(forms.ModelForm):
    date = forms.DateField(initial=datetime.datetime.today)
    #date = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))    
    #currency = SelectFromModel(objects = Currency.objects.all())
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    value = forms.DecimalField()
    
    
    

#Type model
class CategoryForm(forms.ModelForm):
    name = forms.CharField(label='Component type')
    description = forms.CharField(label='Description of type', widget=forms.Textarea())
    name_ukr = forms.CharField(label='Назва (українською)')
    description_ukr = forms.CharField(label='Опис (українською)', widget=forms.Textarea())

    

# --------- Bicycle -------------
    
class BicycleTypeForm(forms.ModelForm):
    type = forms.CharField(label='Bicycle type')
    description = forms.CharField(label='Description of type', widget=forms.Textarea(), max_length=255)


class BicycleFrameSizeForm(forms.ModelForm):
    name = forms.CharField(label='Назва')
    cm = forms.FloatField(min_value=0, label='Розмір, см (cm)')
    inch = forms.FloatField(min_value=0, label='Розмір, дюйми (inch)')
    

class BicycleForm(forms.ModelForm):
    model = forms.CharField(max_length=255)
    type = forms.ModelChoiceField(queryset = Bicycle_Type.objects.all()) #adult, kids, mtb, road, hybrid
    #brand = SelectFromModel(objects=Manufacturer.objects.all())
    brand = forms.ModelChoiceField(queryset = Manufacturer.objects.all())
    #year = forms.DateField(initial=datetime.date.today, input_formats=("%d.%m.%Y"), widget=forms.DateTimeInput(format='%d.%m.%Y'))
    year = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))    
    color = forms.CharField(max_length=255)
    #sizes = forms.MultipleChoiceField()
    sizes = forms.CharField(required=False)
    photo = forms.ImageField()
    weight = forms.FloatField(min_value=0)
    price = forms.FloatField()
    #currency = SelectFromModel(objects=Currency.objects.all())
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)    

    class Meta:
        model = Bicycle
    
    

class BicycleStoreForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset = Bicycle.objects.all(), required=False)
    serial_number = forms.CharField(max_length=50)
    size = forms.ModelChoiceField(queryset = FrameSize.objects.all())
    price = forms.FloatField()
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    count = forms.IntegerField(min_value=0, initial = 1)
    realization = forms.BooleanField(required=False)
    date = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)
    
    class Meta:
        model = Bicycle_Store


class BicycleSaleForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset = Bicycle_Store.objects.all(), required=False)
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    price = forms.FloatField()
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    service = forms.BooleanField(required=False) 
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)
    
    class Meta:
        model = Bicycle_Sale


class BicycleOrderForm(forms.ModelForm):
    model = forms.ModelChoiceField(queryset = Bicycle.objects.all())
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    size = forms.CharField(max_length=50)
    price = forms.FloatField()
    sale = forms.IntegerField()
    prepay = forms.FloatField()
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    done = forms.BooleanField(required=False) 
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)
    
    class Meta:
        model = Bicycle_Order

    
# --------- Dealers ------------
class DealerForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    country = forms.ModelChoiceField(queryset = Country.objects.all())
    city = forms.CharField()
    street = forms.CharField()
    www = forms.URLField()
    description = forms.CharField(label='Description of type', widget=forms.Textarea())
    director = forms.CharField()


class DealerManagerForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField()
    description = forms.CharField(label='Description', widget=forms.Textarea())
    company = forms.ModelChoiceField(queryset = Dealer.objects.all())
    #company = SelectFromModel(objects=Dealer.objects.all())


class DealerPaymentForm(forms.ModelForm):
    dealer_invoice = forms.ModelChoiceField(queryset = DealerInvoice.objects.filter(payment=False))
    invoice_number = forms.CharField(max_length=255)
    date = forms.DateField(initial = datetime.date.today)
    bank = forms.ModelChoiceField(queryset = Bank.objects.all())
    price = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    letter = forms.BooleanField(initial = False, required=False)
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)
  

class DealerInvoiceForm(forms.ModelForm):
    origin_id = forms.CharField(max_length=255, label='Номер накладної')
    date = forms.DateTimeField(initial = datetime.date.today, label='Дата', input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    company = forms.ModelChoiceField(queryset = Dealer.objects.all())
    manager = forms.ModelChoiceField(queryset = DealerManager.objects.all())
    price = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    file = forms.CharField(max_length=255)
    received = forms.BooleanField(initial = False, required=False) 
    payment = forms.BooleanField(initial = False, required=False)
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)


class InvoiceComponentListForm(forms.ModelForm):
    invoice = forms.ModelChoiceField(queryset = DealerInvoice.objects.filter(id=187))
    catalog = forms.ModelChoiceField(queryset = Catalog.objects.none(), required=False)
    #catalog = forms.ModelChoiceField(queryset = Catalog.objects.filter(manufacturer=36))
    count = forms.IntegerField(min_value=0, initial = 1)
    price = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    date = forms.DateTimeField(initial = datetime.date.today, label='Дата', input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        #self.default_username = default_username
        test1 = kwargs.pop('test1', None)
        catalog_id = kwargs.pop('catalog_id', None)
        super(InvoiceComponentListForm, self).__init__(*args, **kwargs)
        if test1<>None:
            self.fields['catalog'].queryset = Catalog.objects.filter(manufacturer = test1) 
        if catalog_id<>None:
            self.fields['catalog'].queryset = Catalog.objects.filter(id = catalog_id)             


class InvoiceComponentForm(forms.ModelForm):
    invoice = forms.ModelChoiceField(queryset = DealerInvoice.objects.all(), required=False)
    #catalog = forms.ModelChoiceField(queryset = Catalog.objects.all())
    #catalog = forms.ModelChoiceField(queryset = Catalog.objects.defer(None))
    catalog = forms.ChoiceField()
    count = forms.IntegerField(min_value=0, initial = 1)
    price = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    date = forms.DateTimeField(initial = datetime.date.today, label='Дата', input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(InvoiceComponentForm, self).__init__( *args, **kwargs)
        instance = kwargs.get('instance')
        CHOICES = (
            (item.id, item.name) for item in  Catalog.objects.all()
         )
        choices_field = forms.ChoiceField(choices=CHOICES)
        self.fields['catalog'] = choices_field
    class Meta:
        model = InvoiceComponentList
        fields = ("id", "ids", "name")

  
class ContactForm(forms.ModelForm):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea())
    sender = forms.EmailField(required=False)


# --------- Product Catalog ------------

class CatalogForm(forms.ModelForm):
    ids = forms.CharField(max_length=50)
    name = forms.CharField(max_length=255)
    manufacturer = forms.ModelChoiceField(queryset = Manufacturer.objects.all())
    type = forms.ModelChoiceField(queryset = Type.objects.all())
    size = forms.ModelChoiceField(queryset = Size.objects.all(), required=False)
    weight = forms.FloatField(min_value=0, required=False)
    photo = forms.ImageField(required=False)
    color = forms.CharField(max_length=255)
    year = forms.IntegerField(initial = 2011, min_value = 1900, max_value = 2020)
    sale = forms.FloatField(initial=0)
    #sale_to = forms.DateField(initial=datetime.date.today)
    sale_to = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    price = forms.FloatField(min_value=0)
    currency = forms.ModelChoiceField(initial = 3, queryset = Currency.objects.all())
    country = forms.ModelChoiceField(queryset = Country.objects.all())    
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255, required=False)    

    class Meta:
        model = Catalog



# ---------- Client -------------
class ClientForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    forumname = forms.CharField(max_length=255, required=False)    
    country = forms.ModelChoiceField(queryset = Country.objects.all())
    city = forms.CharField(max_length=255)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=255, required=False)
    sale = forms.IntegerField(required=False, initial=0)
    summ = forms.FloatField(initial=0)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255, required=False)    

    class Meta:
        model = Client


class ClientDebtsForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today)
    price = forms.FloatField()
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = ClientDebts

   

class ClientCreditsForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today)
    price = forms.FloatField()
    description = forms.CharField(label='DescripCred', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = ClientCredits


class ClientInvoiceForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    #catalog = forms.ModelChoiceField(queryset = Catalog.objects.filter(manufacturer=36))
    catalog = forms.ModelChoiceField(queryset = Catalog.objects.all())    
    count = forms.IntegerField(min_value=0, initial = 1)
    sum = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    sale = forms.IntegerField(min_value=0, initial = 0)
    pay = forms.FloatField(initial=0)
    date = forms.DateTimeField(initial = datetime.date.today, label='Дата', input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        cid = kwargs.pop('catalog_id', None)
        super(ClientInvoiceForm, self).__init__(*args, **kwargs)
        self.fields['catalog'].queryset = Catalog.objects.filter(id = cid)
         



class CostTypeForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    
 
    class Meta:
        model = CostType


    
class CostsForm(forms.ModelForm):
    #date = forms.DateTimeField(initial=datetime.date.today)
    date = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    cost_type = forms.ModelChoiceField(queryset = CostType.objects.all())
    price = forms.FloatField()
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = Costs



# ================== WorkShop ==========================
class WorkGroupForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea()) 

    class Meta:
        model = WorkGroup

        
class WorkTypeForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    work_group = forms.ModelChoiceField(queryset = WorkGroup.objects.all())
    price = forms.FloatField()
    description = forms.CharField(label='Description', widget=forms.Textarea())
    
    class Meta:
        model = WorkType
    

class WorkShopForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    date = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'), required=False)
    work_type = forms.ModelChoiceField(queryset = WorkType.objects.all())
    price = forms.FloatField(initial=0)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255, required=False)
    
    class Meta:
        model = WorkShop


class WorkStatusForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)
    
    class Meta:
        model = WorkStatus


class WorkTicketForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    #date = forms.DateTimeField(initial=datetime.date.today)
    date = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))    
    #end_date = forms.DateTimeField(initial=datetime.date.today)
    end_date = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    status = forms.ModelChoiceField(queryset = WorkStatus.objects.all())
    description = forms.CharField(label='Ticket', widget=forms.Textarea())
    
    class Meta:
        model = WorkTicket


class ShopDailySalesForm(forms.ModelForm):
    #date = forms.DateTimeField(initial=datetime.date.today)
    date = forms.DateField(initial=datetime.date.today, input_formats=['%d.%m.%Y', '%d/%m/%Y'], widget=forms.DateTimeInput(format='%d.%m.%Y'))
    price = forms.FloatField(initial=0)    
    description = forms.CharField(label='description', widget=forms.Textarea())
    
    class Meta:
        model = ShopDailySales


class PreOrderForm(forms.ModelForm):
    date = forms.DateTimeField(initial = datetime.date.today, label='Дата замовлення')
    date_pay = forms.DateTimeField(initial = datetime.date.today, label='Кінцева дата внесення предоплати')
    date_delivery = forms.DateTimeField(initial = datetime.date.today, label='Дата поставки')
    company = forms.ModelChoiceField(queryset = Dealer.objects.all())
    manager = forms.ModelChoiceField(queryset = DealerManager.objects.all(), required=False)
    price = forms.FloatField(initial=0)
    price_pay = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    file = forms.CharField(max_length=255)
    received = forms.BooleanField(initial = False, required=False) 
    payment = forms.BooleanField(initial = False, required=False)
    #payment = forms.ModelChoiceField(queryset = DealerPayment.objects.all())
    description = forms.CharField(label='Description', widget=forms.Textarea(), required=False)

    class Meta:
        model = PreOrder

