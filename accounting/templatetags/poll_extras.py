# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.filter(name='mul')
def mul(value, arg):
    return value * arg

@register.filter
def div(value, arg):
    return value / arg

@register.filter
def sub(value, arg):
    return value / arg


