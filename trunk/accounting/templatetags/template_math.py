# -*- coding: utf-8 -*-
from django import template
import MySQLdb

import datetime
from decimal import *


register = template.Library()
import re

@register.filter(name='mul')
def mul(value, arg):
    return round(float(value) * float(arg), 2)

@register.filter
def div(value, arg):
    '''Деление'''
    return round(float(value) / float(arg), 2)

@register.filter
def sub(value, arg):
    '''Вычитание'''
    return round(float(value) - float(arg), 2)

@register.filter
def summa(value, arg):
    value = 0
    value = float(value) + float(arg)
    return round(value,2)

@register.filter
def dictsumm(value, arg):
    v = 0
    q = arg
    for t in value:
        v = v + t['count']
    
    #value = float(value) + float(arg)
    return value
    #return sum(d.get(arg) for d in value)

@register.filter(name='percentage')  
def percentage(sum, percent):  
    try:  
        a_percent = (100 - float(percent)) / 100.0
        return "%.2f" % (float(sum) * a_percent)  
    except ValueError:  
        return ''  
