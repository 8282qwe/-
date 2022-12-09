from django import template

register = template.Library()


@register.simple_tag
def convert_int(a, b):
    value1 = int(a) * (100 - int(b)) / 100
    return value1
