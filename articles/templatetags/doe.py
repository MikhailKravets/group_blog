from django import template

register = template.Library()


@register.simple_tag
def print(value: str):
    return f"<b>{value.upper()}</b>"
