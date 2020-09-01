from django import template

register = template.Library()


@register.filter
def inc(value, increment):
    return str(int(value) + int(increment))


@register.simple_tag
def division(divised, divider,to_int=False):
    res = int(divised) / int(divider)
    if to_int:
        res = int(res)

    return str(res)
