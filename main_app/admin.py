from django.contrib import admin
import main_app.models as _
from django.contrib.auth.admin import UserAdmin
from main_app.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

# TODO: ¿Todos los usuarios q no sean superuser pueden acceder al admin site? O hay q hacer algo especifico para q solo lo q sean super user o tengan los perisos de gestion de usuario puedan acceder al django admin


class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'name', 'apellidos',
                    'ci', 'tfno', 'apto', 'is_staff', 'is_admin_fabrim', 'is_customer',)
    list_filter = ('is_staff', 'is_admin_fabrim',)
    fieldsets = (
        (None, {'fields': ('name', 'apellidos',
         'email', 'ci', 'tfno', 'apto', 'password', 'groups', 'user_permissions')}),
        ('permissions', {
         'fields': ('is_staff', 'is_customer', 'is_superuser', 'is_admin_fabrim')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'apellidos', 'ci', 'tfno', 'apto', 'groups', 'user_permissions', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', )
    filter_horizontal = ()


admin.site.register(_.User, CustomUserAdmin)
# admin.site.register(_.TipoMedicamento)
