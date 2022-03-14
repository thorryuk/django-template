from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def trim(value):
    return value.strip()


@register.filter(name='compare_dict')
def compare_dict(key, dict):
    if key in dict:
        return 'checked'
    return ''
