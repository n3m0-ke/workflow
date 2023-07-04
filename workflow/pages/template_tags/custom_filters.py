from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name="date_difference")
def date_difference(value, arg):
    if value and arg:
        return (arg - value).days
    return None
