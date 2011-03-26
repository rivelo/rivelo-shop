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