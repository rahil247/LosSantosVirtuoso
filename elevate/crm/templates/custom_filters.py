from django import template

register = template.Library()

@register.filter(name='add_placeholder')
def add_placeholder(field, placeholder_text):
    field.field.widget.attrs.update({'placeholder': placeholder_text})
    return field
