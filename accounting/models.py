# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin

# Type = Component category 
class Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]    


# Size catalog
class Size(models.Model):
    name = models.CharField(max_length=100)
    width = models.IntegerField() 
    hight = models.IntegerField()
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]    


# Country table (Country)
class Country(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]    


class Bank(models.Model):
    name = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]    


# list of currency
class Currency(models.Model):
    ids = models.CharField("code", max_length=50)
    #поле скорочена назва валюти
    ids_char = models.CharField("code", unique=True, max_length=5)
    name = models.CharField("currency name", max_length=50)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["ids"]    



# exchange rate
class Exchange(models.Model):
    date = models.DateTimeField()
    currency = models.ForeignKey(Currency)    
    value = models.DecimalField("money", max_digits=5, decimal_places=2)
    
    def __unicode__(self):
        return self.currency

    class Meta:
        ordering = ["date"]    


# list of manufectures 
class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    www = models.URLField(verify_exists=False, blank=True, null=True)
    logo = models.ImageField(upload_to = 'media/upload/', blank=True, null=True)
    country = models.ForeignKey(Country, null=True)
    
    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ["name"]    


# Main table 
class Catalog(models.Model):
    ids = models.CharField("code", unique=True, max_length=50)
    name = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer)
    type = models.ForeignKey(Type, related_name='type')
    size = models.ForeignKey(Size, blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)    
    photo = models.FileField(upload_to = 'media/upload/catalog/%Y/%m/%d', null=True)
    year = models.IntegerField(blank=True, null=True)
    sale_to = models.DateField(auto_now_add=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    #count = models.IntegerField("how many something", default=1)
    #price = models.FloatField()
    sale = models.FloatField()
    country = models.ForeignKey(Country, null=True)
    description = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["type", "name"]    


# Bill table (nakladna)
class Bill(models.Model):
    ids = models.CharField("code", unique=True, max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Catalog)
    count = models.IntegerField("how many something", default=1)
    price = models.FloatField(blank=True, null=True)
    currency = models.ForeignKey(Currency)
    description = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["ids"]    


# Check table (Check)
class Check(models.Model):
    ids = models.CharField("code", unique=True, max_length=50)
    date = models.DateTimeField()
    product = models.ForeignKey(Catalog)
    count = models.IntegerField("how many something", default=1)
    price = models.FloatField()
    description = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["ids"]    


# Frame Size
class FrameSize(models.Model):
    name = models.CharField(max_length=100)
    cm = models.FloatField() 
    inch = models.FloatField()
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["inch","name"]    




# postach Dealer (Ukraine)
class Dealer(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
#    brand = models.ManyToManyFields(Manufacturer)
    www = models.URLField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    
    
    def __unicode__(self):
        #return self.name
        return u'Країна %s' % self.name

    class Meta:
        ordering = ["name"]    


# postach Dealer (Ukraine)
class DealerManager(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=100)
    company = models.ForeignKey(Dealer)
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["company", "name"]    


# Dealer payment (Ukraine)
class DealerPayment(models.Model):
    invoice_number = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    bank = models.ForeignKey(Bank)
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    description = models.TextField(blank = True, null = True)
            
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["invoice_number", "date"]    


# Dealer invoice (Ukraine)
class DealerInvoice(models.Model):
    origin_id = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Dealer)
    manager = models.ForeignKey(DealerManager, blank = True, null = True)
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    file = models.CharField(max_length=255)
    received = models.BooleanField(default=False, verbose_name="Товар отримано?", blank = True, null = True)
    payment = models.ForeignKey(DealerPayment, blank = True, null = True)
    description = models.TextField(blank = True, null = True)
            
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["company", "date"]    


#Client database
class Client(models.Model):
    name = models.CharField(max_length=255)
    forumname = models.CharField(max_length=255)
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    sale = models.IntegerField("how many percent for sale", default=0)
    summ = models.FloatField()
    description = models.TextField()

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]    


class ClientDebts(models.Model):
    client = models.ForeignKey(Client)
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    description = models.TextField()

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["client", "date"]    


class ClientCredits(models.Model):
    client = models.ForeignKey(Client)
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    description = models.TextField()

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["client", "date"]    


#my costs (Затрати)
class CostType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]    


class Costs(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    cost_type = models.ForeignKey(CostType)
    price = models.FloatField()
    description = models.TextField()

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["date"]



#Bicycle type table
class Bicycle_Type(models.Model):
    type = models.CharField(max_length=255) #adult, kids, mtb, road, hybrid
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.type

    class Meta:
        ordering = ["type"]    


# Bicycle table (Bicycle)
class Bicycle(models.Model):
    model = models.CharField(max_length=255)
    type = models.ForeignKey(Bicycle_Type) #adult, kids, mtb, road, hybrid
    brand = models.ForeignKey(Manufacturer)
#    year = models.DateField(input_formats=("%d/%m/%Y",))
    color = models.CharField(max_length=255)
    #sizes = models.CharField(max_length=255)    
    sizes = models.CommaSeparatedIntegerField(max_length=10)
    photo = models.ImageField(upload_to = 'media/upload/', max_length=255)
    weight = models.FloatField()
    #PositiveIntegerField()
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        #return u'Велосипед %s. Ціна %s грн.' % (self.model, self.brand)
        return u'Велосипед %s. Модель %s' % (self.brand, self.model)
        #return u'Велосипед %s. Ціна %d грн.' % (self.model, self.price)
        
    class Meta:
        ordering = ["model", "price"]    
       
        
# Bicycle in store (BicycleStore)
class Bicycle_Store(models.Model):
    model = models.ForeignKey(Bicycle, blank = True, null = True)
    serial_number = models.CharField(max_length=50)
    size = models.ForeignKey(FrameSize, blank = True, null = True)
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    description = models.TextField(blank=True, null=True)
    realization = models.BooleanField() 
    count = models.PositiveIntegerField()
    
    def __unicode__(self):
        #return self.model
        return u'%s' % self.model

    class Meta:
        ordering = ["model"]    
# Bicycle sale to client
class Bicycle_Sale(models.Model):
    model = models.ForeignKey(Bicycle_Store)
    client = models.ForeignKey(Client)
    price = models.FloatField()
    currency = models.ForeignKey(Currency)
    date = models.DateField(auto_now_add=True)
    service = models.BooleanField(default = True) 
    description = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        #return self.model
        return u'%s' % self.model

    class Meta:
        ordering = ["client", "model"]    
class WorkGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

     
class WorkType(models.Model):
    name = models.CharField(max_length=255)
    work_group = models.ForeignKey(WorkGroup)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
     
    
class WorkShop(models.Model):
    client = models.ForeignKey(Client)
    date = models.DateTimeField(auto_now_add=True)
    work_type = models.ForeignKey(WorkType)
    price = models.FloatField()
    description = models.TextField(blank=True, null=True)

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["date"]


class WorkStatus(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
       

class WorkTicket(models.Model):
    client = models.ForeignKey(Client)
    date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    status = models.ForeignKey(WorkStatus)
    description = models.TextField(blank=True, null=True)

    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["date", "status"]
