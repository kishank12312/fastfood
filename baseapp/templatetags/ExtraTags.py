from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def productqty(value, arg):
    for i in value:
        if i.ProductID == arg:
            return i.Quantity
    return "F"