from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
import main_app.models as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

login_msgs = {
    'invalid': 'Existen datos incorrectos'
}

required_forms = {
    "required": "Este campo es requerido"
}


class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Acceso denegado.",
        'inactive': "Esta cuenta está inactiva.",
        'required': 'Este campo es requerido.',
    }

    username = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control form-control-lg'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña...',
            'id': 'password1',
        }
    ))
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ingrese la contraseña nuevamente...',
            'id': 'password1',
        }
    ))

    class Meta:
        model = User
        fields = ['name', 'apellidos', 'ci', 'tfno', 'apto', 'email']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese el nombre...'}),
            'apellidos': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese los apellidos...'}),
            'ci': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese el carnet de identidad...'}),
            'tfno': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese su número telefónico...'}),
            'apto': forms.TextInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese su apartamento...'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control form-control-lg', 'placeholder': 'Ingrese su correo...'}),
        }
        error_messages = {
            'email': {
                'required': "Este campo es requerido.",
                'invalid': "Correo invalido"
            },
            'name': {
                'required': "Este campo es requerido.",
            },
            'apellidos': {
                'required': "Este campo es requerido.",
            },
            'ci': {
                'required': "Este campo es requerido.",
            },
            'tfno': {
                'required': "Este campo es requerido.",
            },
            'apto': {
                'required': "Este campo es requerido.",
            },
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        if len(password1) < 8:
            raise forms.ValidationError(
                'La contraseña debe tener al menos 8 caracteres')
        return password2

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("El correo ya existe")
        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.is_customer = True
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        user.groups.add(Group.objects.get(name="Cliente"))
        return user


class MedicamentosForm(forms.ModelForm):
    class Meta:
        model = _.Medicamento
        fields = ('__all__')
        error_messages = {
            'nombre': {
                'required': "Este campo es requerido.",
            },
            'no_lote': {
                'required': "Este campo es requerido.",
                'unique': "Número de lote existente"

            },
            'fecha_cad': {
                'required': "Este campo es requerido.",
            },
            'tarjeta_estiba_id': {
                'required': "Este campo es requerido.",
            },
            'tipo_medicamento_id': {
                'required': "Este campo es requerido.",
            },
        }


class TarjetaEstibaForm(forms.ModelForm):
    class Meta:
        model = _.TarjetaEstiba
        fields = ('__all__')
        error_messages = {
            'no_serie': {
                'required': "Este campo es requerido.",
                'unique': "Número de serie existente"

            },
            'precio': {
                'required': "Este campo es requerido.",
                'invalid': "Los datos no son correctos",
            },
            'cant_medi': {
                'required': "Este campo es requerido.",
                'invalid': "Los datos no son correctos"
            },
        }

    def clean_precio(self):
        data = self.cleaned_data.get("precio")

        if data <= 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo o cero.")

        return data

    def clean_cant_medi(self):
        data = self.cleaned_data.get("cant_medi")

        if data <= 0:
            raise forms.ValidationError(
                "La cantidad no puede ser negativa o cero.")

        return data


class PedidoForm(forms.ModelForm):
    class Meta:
        model = _.Pedido
        fields = ('__all__')
        error_messages = {
            'cantidad_medicamento': {
                'required': "Este campo es requerido.",
                'invalid': "Los datos no son correctos"
            },
            'medicamento_id': {
                'required': "Este campo es requerido.",
            }
        }

    def clean_cantidad_medicamento(self):
        data = self.cleaned_data.get("cantidad_medicamento")

        if data <= 0:
            raise forms.ValidationError(
                "La cantidad no puede ser negativa o cero.")

        return data


class CompraForm(forms.ModelForm):
    class Meta:
        model = _.Compra
        fields = ['tarjeta_bancaria', 'cantidad']
        error_messages = {
            'cantidad': {
                'required': "Este campo es requerido.",
                'invalid': "Los datos no son correctos",

            },
            'tarjeta_bancaria': {
                'required': "Este campo es requerido.",
            }
        }

    def clean_cantidad(self):
        data = self.cleaned_data.get("cantidad")

        if data <= 0:
            raise forms.ValidationError(
                "La cantidad no puede ser negativa o cero.")

        return data


class UserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, error_messages={
                                'required': "Este campo es requerido.", })
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput, error_messages={'required': "Este campo es requerido.", })

    class Meta:
        model = User
        fields = ('__all__')
        error_messages = {
            'email': {
                'required': "Este campo es requerido.",
                'invalid': "Correo invalido",
                'unique': "Correo existente"
            },
            'name': {
                'required': "Este campo es requerido.",
            },
            'apellidos': {
                'required': "Este campo es requerido.",
            },
            'ci': {
                'required': "Este campo es requerido.",
                'unique': "Carnet de identidad existente"
            },
            'tfno': {
                'required': "Este campo es requerido.",
                'unique': "Telefono existente"
            },
            'apto': {
                'required': "Este campo es requerido.",
            },
        }

    def clean_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        if len(password1) < 8:
            raise forms.ValidationError(
                'La contraseña debe tener al menos 8 caracteres')
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('__all__')
        error_messages = {
            'email': {
                'required': "Este campo es requerido.",
                'invalid': "Correo invalido",
                'unique': "Correo existente"
            },
            'name': {
                'required': "Este campo es requerido.",
            },
            'apellidos': {
                'required': "Este campo es requerido.",
            },
            'ci': {
                'required': "Este campo es requerido.",
                'unique': "Carnet de identidad existente"
            },
            'tfno': {
                'required': "Este campo es requerido.",
            },
            'apto': {
                'required': "Este campo es requerido.",
            },
        }
