# -*- coding: utf-8 -*-
from django import template
import MySQLdb

import datetime
from decimal import *




register = template.Library()
import re

@register.filter(name='mul')
def mul(value, arg):
    return float(value) * float(arg)

@register.filter
def div(value, arg):
    '''Деление'''
    return value / arg

@register.filter
def sub(value, arg):
    '''Вычитание'''
    return value / arg