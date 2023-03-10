from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)

    if group:
        group = group.first()
        return True if group in user.groups.all() or user.is_superuser == True else False
    else:
        return False
