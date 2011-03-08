# -*- coding: utf-8 -*-

from django.contrib import admin
from catalog.accounting.models import Type, Size, Exchange, Manufacturer, Catalog, Country, Dealer, Currency, Bicycle_Type



class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name', 'description')
    ordering = ('-name',)
    search_fields = ('name', 'description')
  
admin.site.register(Type, TypeAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-name',)
    search_fields = ('name',)

admin.site.register(Country, CountryAdmin)


class DealerAdmin(admin.ModelAdmin):
    list_display = ('name','country', 'city', 'street', 'www', 'description', 'director')
    ordering = ('-name',)
    search_fields = ('name',)

admin.site.register(Dealer, DealerAdmin)


class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'hight')
    list_filter = ('name', 'width', 'hight')
    ordering = ('-name',)
    search_fields = ('name',)

admin.site.register(Size, SizeAdmin)

class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('date', 'currency', 'value')
    list_filter = ('date', 'currency', 'value')
    ordering = ('-date',)
    search_fields = ('date',)

admin.site.register(Exchange, ExchangeAdmin)

	
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'www', 'country')
    ordering = ('name', 'description', 'www', 'country')
    search_fields = ('name',)

admin.site.register(Manufacturer, ManufacturerAdmin)


class CatalogAdmin(admin.ModelAdmin):
    list_display = ('ids', 'name', 'manufacturer', 'type', 'size', 'photo', 'weight', 'sale', 'country', 'description')
    ordering = ('-name',)
    search_fields = ('ids', 'name',)

admin.site.register(Catalog, CatalogAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('ids', 'ids_char', 'name', 'country')
    ordering = ('-ids',)
    search_fields = ('ids', 'name',)
    
admin.site.register(Currency, CurrencyAdmin)
    

class Bicycle_TypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'description')
    ordering = ('-type',)
    search_fields = ('type',)

admin.site.register(Bicycle_Type, Bicycle_TypeAdmin)    












