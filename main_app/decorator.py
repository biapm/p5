from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group


def for_customer(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check logged in user could be a customer and redirects to the login page if the user isn't authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_customer or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def for_staff(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check whether the logged-in user is staff and 
    redirect to the login page if the user is not authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff or u.is_admin_fabrim or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def for_admin_or_dependiente(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check whether the logged-in user is an Administrador or Dependiente and 
    redirect to the login page if the user is not authenticated.
    '''
    group = Group.objects.filter(name="Administrador").first()
    group1 = Group.objects.filter(name="Dependiente").first()

    actual_decorator = user_passes_test(
        lambda u: u.is_active and (group in u.groups.all()) or (
            group1 in u.groups.all()) or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def for_almacenero(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check whether the logged-in user is an Almacenero and 
    redirect to the login page if the user is not authenticated.
    '''
    group = Group.objects.filter(name="Almacenero").first()
    actual_decorator = user_passes_test(
        lambda u: u.is_active and (group in u.groups.all()) or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def for_all_to_view(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check whether the logged-in user is an role in system and 
    redirect to the login page if the user is not authenticated.
    '''
    group = Group.objects.filter(name="Almacenero").first()
    group1 = Group.objects.filter(name="Dependiente").first()
    group2 = Group.objects.filter(name="Administrador").first()

    actual_decorator = user_passes_test(
        lambda u: u.is_active and (group in u.groups.all()) or (
            group2 in u.groups.all()) or (group1 in u.groups.all()) or u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
