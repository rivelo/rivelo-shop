# -*- coding: utf-8 -*-
from django import forms
from models import Manufacturer, Country, Type, Bicycle_Type, Bicycle, Currency, FrameSize, Bicycle_Store, Catalog, Size, Bicycle_Sale 
from models import DealerManager, DealerPayment, DealerInvoice, Dealer, Bank
from models import Client, ClientDebts, CostType, Costs, ClientCredits, WorkGroup, WorkType, WorkShop, WorkTicket, WorkStatus

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



class ManufacturerForm(forms.Form):
    name = forms.CharField()
    www = forms.URLField(initial='http://', help_text='url')
    #country = forms.CharField(widget=forms.Select())
    country = SelectFromModel(objects=Country.objects.all())
    logo = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea())

class CountryForm(forms.Form):
    name = forms.CharField(label='Country name')


class BankForm(forms.Form):
    name = forms.CharField(label='Bank name')


class CurencyForm(forms.Form):
    ids = forms.CharField()
    ids_char = forms.CharField()
    name = forms.CharField()
    country = SelectFromModel(objects=Country.objects.all())



class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object - %i" % obj.name

import datetime

class ExchangeForm(forms.Form):
    date = forms.DateField(initial=datetime.date.today)
    #currency = SelectFromModel(objects = Currency.objects.all())
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    value = forms.DecimalField()
    

#Type model
class CategoryForm(forms.Form):
    name = forms.CharField(label='Component type')
    description = forms.CharField(label='Description of type', widget=forms.Textarea(), max_length=255)
    

# --------- Bicycle -------------
    
class BicycleTypeForm(forms.Form):
    type = forms.CharField(label='Bicycle type')
    description = forms.CharField(label='Description of type', widget=forms.Textarea(), max_length=255)


class BicycleFrameSizeForm(forms.Form):
    name = forms.CharField(label='Bicycle Frame Size')
    cm = forms.FloatField(min_value=0)
    inch = forms.FloatField(min_value=0)
    

class BicycleForm(forms.Form):
    model = forms.CharField(max_length=255)
    type = forms.ModelChoiceField(queryset = Bicycle_Type.objects.all()) #adult, kids, mtb, road, hybrid
    #brand = SelectFromModel(objects=Manufacturer.objects.all())
    brand = forms.ModelChoiceField(queryset = Manufacturer.objects.all())
#    year = models.DateField(input_formats=("%d/%m/%Y",))
    color = forms.CharField(max_length=255)
    #sizes = forms.MultipleChoiceField()
    sizes = forms.CharField()
    photo = forms.ImageField()
    weight = forms.FloatField(min_value=0)
    price = forms.FloatField()
    #currency = SelectFromModel(objects=Currency.objects.all())
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = Bicycle
    
    

class BicycleStoreForm(forms.Form):
    model = forms.ModelChoiceField(queryset = Bicycle.objects.all(), required=False)
    #model_id = forms.ModelChoiceField(queryset = Bicycle.objects.all())
    #model = forms.ModelChoiceField(queryset = FrameSize.objects.all())
    
    serial_number = forms.CharField(max_length=50)
    size = forms.ModelChoiceField(queryset = FrameSize.objects.all())
    price = forms.FloatField()
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    description = forms.CharField()
    realization = forms.BooleanField(required=False) 
    count = forms.IntegerField(min_value=0)

    class Meta:
        model = Bicycle_Store


class BicycleSaleForm(forms.Form):
    model = forms.ModelChoiceField(queryset = Bicycle_Store.objects.all(), required=False)
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    price = forms.FloatField()
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today)
    service = forms.BooleanField(required=False) 
    description = forms.CharField(label='Description', widget=forms.Textarea())
    
    class Meta:
        model = Bicycle_Sale

    
# --------- Dealers ------------
class DealerForm(forms.Form):
    name = forms.CharField(max_length=255)
    country = forms.ModelChoiceField(queryset = Country.objects.all())
    city = forms.CharField()
    street = forms.CharField()
    www = forms.URLField()
    description = forms.CharField(label='Description of type', widget=forms.Textarea())
    director = forms.CharField()


class DealerManagerForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField()
    description = forms.CharField(label='Description', widget=forms.Textarea())
    company = forms.ModelChoiceField(queryset = Dealer.objects.all())
    #company = SelectFromModel(objects=Dealer.objects.all())


class DealerPaymentForm(forms.Form):
    invoice_number = forms.CharField(max_length=255)
    date = forms.DateField(initial = datetime.date.today)
    bank = forms.ModelChoiceField(queryset = Bank.objects.all())
    price = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    description = forms.CharField(label='Description', widget=forms.Textarea())
  

class DealerInvoiceForm(forms.Form):
    origin_id = forms.CharField(max_length=255, label='Номер накладної')
    date = forms.DateTimeField(initial = datetime.date.today, label='Дата')
    company = forms.ModelChoiceField(queryset = Dealer.objects.all())
    manager = forms.ModelChoiceField(queryset = DealerManager.objects.all(), required=False)
    price = forms.FloatField(initial=0)
    currency = forms.ModelChoiceField(queryset = Currency.objects.all())
    file = forms.CharField(max_length=255)
    received = forms.BooleanField(initial = False, required=False) 
    payment = forms.ModelChoiceField(queryset = DealerPayment.objects.all(), required=False)
    description = forms.CharField(label='Description', widget=forms.Textarea())
        
    
class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea())
    sender = forms.EmailField(required=False)



# --------- Product Catalog ------------

class CatalogForm(forms.Form):
    ids = forms.CharField(max_length=50)
    name = forms.CharField(max_length=255)
    manufacturer = forms.ModelChoiceField(queryset = Manufacturer.objects.all())
    type = forms.ModelChoiceField(queryset = Type.objects.all())
    size = forms.ModelChoiceField(queryset = Size.objects.all())
    weight = forms.FloatField(min_value=0)
    photo = forms.ImageField()
    year = forms.IntegerField(min_value = 1900, max_value = 2020)
    sale = forms.FloatField()
    sale_to = forms.DateField(initial=datetime.date.today)
    color = forms.CharField(max_length=255)
    country = forms.ModelChoiceField(queryset = Country.objects.all())    
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = Catalog



# ---------- Client -------------
class ClientForm(forms.Form):
    name = forms.CharField(max_length=255)
    forumname = forms.CharField(max_length=255, required=False)    
    country = forms.ModelChoiceField(queryset = Country.objects.all())
    city = forms.CharField(max_length=255)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=255, required=False)
    sale = forms.IntegerField(required=False, initial=0)
    summ = forms.FloatField(initial=0)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = Client



class ClientDebtsForm(forms.Form):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today)
    price = forms.FloatField()
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = ClientDebts

   

class ClientCreditsForm(forms.Form):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today)
    price = forms.FloatField()
    description = forms.CharField(label='DescripCred', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = ClientCredits



class CostTypeForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    
 
    class Meta:
        model = CostType


    
class CostsForm(forms.Form):
    date = forms.DateTimeField(initial=datetime.date.today)
    cost_type = forms.ModelChoiceField(queryset = CostType.objects.all())
    price = forms.FloatField()
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)    

    class Meta:
        model = Costs



# ================== WorkShop ==========================
class WorkGroupForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255) 

    class Meta:
        model = WorkGroup

        
class WorkTypeForm(forms.Form):
    name = forms.CharField(max_length=255)
    work_group = forms.ModelChoiceField(queryset = WorkGroup.objects.all())
    price = forms.FloatField()
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)
    
    class Meta:
        model = WorkType
    

class WorkShopForm(forms.Form):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today)
    work_type = forms.ModelChoiceField(queryset = WorkType.objects.all())
    price = forms.FloatField(initial=0)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)
    
    class Meta:
        model = WorkShop


class WorkStatusForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(label='Description', widget=forms.Textarea(), max_length=255)
    
    class Meta:
        model = WorkStatus


class WorkTicketForm(forms.Form):
    client = forms.ModelChoiceField(queryset = Client.objects.all())
    date = forms.DateTimeField(initial=datetime.date.today)
    end_date = forms.DateTimeField(initial=datetime.date.today)
    status = forms.ModelChoiceField(queryset = WorkStatus.objects.all())
    description = forms.CharField(label='Ticket', widget=forms.Textarea())
    
    class Meta:
        model = WorkTicket
