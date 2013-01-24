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


@register.inclusion_tag('orm_debug.html')
def orm_debug():
    import re
    try:
        from pygments import highlight
        from pygments.lexers import SqlLexer
        from pygments.formatters import HtmlFormatter
        pygments_installed = True
    except ImportError:
        pygments_installed = False

    from django.db import connection
    queries = connection.queries
    query_time = 0
    query_count = 0
    for query in queries:
        query_time += float(query['time'])
        query_count += int(1)
        query['sql'] = re.sub(r'(FROM|WHERE)', '\n\\1', query['sql'])
        query['sql'] = re.sub(r'((?:[^,]+,){3})', '\\1\n    ', query['sql'])
        if pygments_installed:
            formatter = HtmlFormatter()
            query['sql'] = highlight(query['sql'], SqlLexer(), formatter)
            pygments_css = formatter.get_style_defs()
        else:
            pygments_css = ''
    return {
        'pygments_css': pygments_css,
        'pygments_installed': pygments_installed,
        'query_time': query_time,
        'query_count': query_count,
        'queries': queries}    
