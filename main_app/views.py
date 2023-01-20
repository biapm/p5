from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
import main_app.forms as _forms
import main_app.models as _models
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import permission_required, login_required
from main_app.decorator import for_staff, for_customer, for_admin_or_dependiente, for_all_to_view, for_almacenero
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate

User = get_user_model()

# TODO:Como hago para q el usuario si es un cliente m mande para la vista de el usuario y sino para la de administacion


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="index")
    elif (request.user.is_staff or request.user.is_admin_fabrim) and request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="/admin-fabrim/principal/")
    elif request.user.is_customer and request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to="/fabrim/medicamentos/")


def login_user(request):
    form = _forms.LoginForm(request.POST or None)

    if request.method == "GET":
        return render(request, 'sign-in/login.html', {'form': form})
    else:
        user = authenticate(
            request, email=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            if user.is_admin_fabrim or user.is_staff:
                messages.success(request, "¡Usuario logueado correctamente!")
                return redirect('principal')
            else:
                messages.success(request, "¡Usuario logueado correctamente!")
                return redirect('index_users')
        else:
            messages.error(request, "Credenciales invalidas")
            return render(request, 'sign-in/login.html', {"icon": "error", 'form': form})


class IndexView(TemplateView):
    template_name = "base.html"


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = "sign-in/register.html"
    form_class = _forms.RegisterForm
    success_url = reverse_lazy('login')
    success_message = "Usuario registrado"

# TODO: Esta es mi vista si el usuario es staff, ya sea cualquiera de las opciones de los staff


@method_decorator([for_staff,], name='dispatch')
class PrincipalTemplateView(LoginRequiredMixin, TemplateView, PermissionRequiredMixin):
    template_name = "administrador_index.html"
    permission_required = 'main_app.view_user'


"""---------------------------------------------------------------
-----------------------------MEDICAMENTOS VIEW ------------------------
---------------------------------------------------------------"""

# TODO: No c si esta manera de hacer lo de los usuarios para privatizar las rutas sea la correcta o sea q a esta ruta y a todas las q tengan este decorador for_staff el usuario no lo deje acceder


@method_decorator([for_staff, for_admin_or_dependiente,], name='dispatch')
class MedicamentosView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    template_name = 'pages/admin_views/medicamentos.html'
    model = _models.Medicamento
    permission_required = "main_app.view_medicamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarjetas_estiba'] = True if _models.TarjetaEstiba.objects.all(
        ) else False
        context['tipos_medicamentos'] = True if _models.TipoMedicamento.objects.all(
        ) else False
        context['title'] = 'Medicamentos'
        return context


@method_decorator([for_staff, for_admin_or_dependiente, ], name='dispatch')
class MedicamentosCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView, PermissionRequiredMixin):
    model = _models.Medicamento
    template_name = 'pages/forms/medicamentos_add.html'
    form_class = _forms.MedicamentosForm
    success_url = reverse_lazy('medicamentos')
    success_message = 'Medicamento creado correctamente!'
    permission_required = "main_app.add_medicamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarjetas_estiba'] = _models.TarjetaEstiba.objects.all()
        context['tipos_medicamentos'] = _models.TipoMedicamento.objects.all()
        context['title'] = 'Agregar Medicamento'
        return context


@method_decorator([for_staff, for_admin_or_dependiente,], name='dispatch')
class MedicamentosEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView, PermissionRequiredMixin):
    model = _models.Medicamento
    template_name = 'pages/forms/medicamentos_edit.html'
    form_class = _forms.MedicamentosForm
    success_url = reverse_lazy('medicamentos')
    success_message = 'Medicamento modificado correctamente!'
    permission_required = "main_app.change_medicamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarjetas_estiba'] = _models.TarjetaEstiba.objects.all()
        context['tipos_medicamentos'] = _models.TipoMedicamento.objects.all()
        context['title'] = 'Editar Medicamento'
        return context


@method_decorator([for_staff, for_admin_or_dependiente,], name='dispatch')
class MedicamentoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = _models.Medicamento
    template_name = 'pages/forms/medicamentos_delete.html'
    success_url = reverse_lazy('medicamentos')
    success_message = "El medicamento ha sido eliminado"
    permission_required = 'main_app.delete_medicamento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar medicamento'
        return context


"""---------------------------------------------------------------
-----------------------------COMPRAS VIEW ------------------------
---------------------------------------------------------------"""

# TODO: Esta es mi vista si el usuario es comprador, o sea la principal del usuario si es comprador


@method_decorator([for_customer,], name='dispatch')
class MedicamentosListBuy(ListView, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = "pages/users/index_user.html"
    model = _models.Medicamento
    permission_required = "main_app.view_medicamento"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nuestros medicamentos:'
        return context

# TODO: No se si esta sea la manera de privatizar estas function views para q solo sean accesibles si el usuario es un cliente


@for_customer
@login_required(redirect_field_name='login')
@permission_required(('main_app.add_compra', ))
def comprar_medicamento(request, pk):
    context = {}

    medicamento = _models.Medicamento.objects.get(pk=pk)
    context['medicamento'] = medicamento

    form = _forms.CompraForm(request.POST or None)
    if form.is_valid():
        te = _models.TarjetaEstiba.objects.get(pk=pk)
        te.cant_medi -= int(request.POST.get('cantidad'))

        compra = _models.Compra(cantidad=int(request.POST.get('cantidad')), medicamento_id=medicamento,
                                tarjeta_bancaria=request.POST.get('tarjeta_bancaria'), total_pagado=te.precio * int(request.POST.get('cantidad')), usuario_id=User.objects.get(pk=request.user.id))

        te.save()
        compra.save()
        messages.success(request, "¡Medicamento comprado!")
        return redirect('index_users')

    context['form'] = form
    context['title'] = "Comprar"
    return render(request, "pages/forms/compra_add.html", context)


@for_customer
@login_required(redirect_field_name='login')
@permission_required(('main_app.generate_voucher', ))
def generar_comprobante(request, pk):
    context = {}
    context['title'] = "Comprobante de pago:"
    context['object'] = _models.Compra.objects.get(pk=pk)
    return render(request, "pages/forms/compra_comprobante.html", context)


@login_required(redirect_field_name='login')
@for_customer
@permission_required(('main_app.view_compra', ))
def list_own_buys(request):
    context = {}
    context['title'] = "Sus compras"
    context['object_list'] = _models.Compra.objects.filter(
        usuario_id=request.user)

    return render(request, "pages/users/compras_user.html", context)


"""---------------------------------------------------------------
-----------------------------TARJETA ESTIBA VIEW ------------------------
---------------------------------------------------------------"""


@method_decorator([for_staff, for_all_to_view,], name='dispatch')
class TarjetasEstibaView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    template_name = 'pages/admin_views/tarjeta_estiba.html'
    permission_required = "main_app.view_tarjetaestiba"
    model = _models.TarjetaEstiba

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tarjetas de Estiba'
        return context


@method_decorator([for_staff, for_admin_or_dependiente,], name='dispatch')
class TarjetasEstibaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView, PermissionRequiredMixin):
    model = _models.TarjetaEstiba
    template_name = 'pages/forms/tarjetaestiba_add.html'
    form_class = _forms.TarjetaEstibaForm
    success_url = reverse_lazy('tarjetas-estiba')
    success_message = 'Tarjeta Estiba creada correctamente.'
    permission_required = "main_app.add_tarjetaestiba"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar tarjeta de estiba'
        return context


@method_decorator([for_staff, for_admin_or_dependiente,], name='dispatch')
class TarjetasEstibaEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView, PermissionRequiredMixin):
    model = _models.TarjetaEstiba
    template_name = 'pages/forms/tarjetaestiba_edit.html'
    form_class = _forms.TarjetaEstibaForm
    success_url = reverse_lazy('tarjetas-estiba')
    success_message = 'Tarjeta Estiba editada correctamente.'
    permission_required = "main_app.change_tarjetaestiba"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar tarjeta de estiba'
        return context


@method_decorator([for_staff, for_admin_or_dependiente,], name='dispatch')
class TarjetaEstibaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = _models.TarjetaEstiba
    template_name = 'pages/forms/tarjetaestiba_delete.html'
    success_url = reverse_lazy('tarjetas-estiba')
    success_message = "La Tarjeta Estiba ha sido eliminada, asi como el medicamento asociado a la misma"
    permission_required = 'main_app.delete_tarjetaestiba'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar tarjeta estiba'
        return context


"""---------------------------------------------------------------
-----------------------------PEDIDOS VIEW ------------------------
---------------------------------------------------------------"""


@method_decorator([for_staff, for_almacenero,], name='dispatch')
class PedidosView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    template_name = 'pages/admin_views/pedidos.html'
    permission_required = "main_app.view_pedido"
    model = _models.Pedido

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pedidos'
        context['medicamentos'] = True if _models.Medicamento.objects.all() else False
        return context


@method_decorator([for_staff, for_almacenero,], name='dispatch')
class PedidosCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView, PermissionRequiredMixin):
    model = _models.Pedido
    template_name = 'pages/forms/pedidos_add.html'
    form_class = _forms.PedidoForm
    success_url = reverse_lazy('pedidos')
    success_message = 'Pedido creado correctamente.'
    permission_required = "main_app.add_pedido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicamentos'] = _models.Medicamento.objects.all()
        context['title'] = 'Hacer Pedido'
        return context


@method_decorator([for_staff, for_almacenero,], name='dispatch')
class PedidosEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView, PermissionRequiredMixin):
    model = _models.Pedido
    template_name = 'pages/forms/pedidos_edit.html'
    form_class = _forms.PedidoForm
    success_url = reverse_lazy('pedidos')
    success_message = 'Pedido editado correctamente.'
    permission_required = "main_app.change_pedido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicamentos'] = _models.Medicamento.objects.all()
        context['title'] = 'Cambiar Pedido'
        return context


@method_decorator([for_staff, for_almacenero,], name='dispatch')
class PedidosDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = _models.Pedido
    template_name = 'pages/forms/pedidos_delete.html'
    success_url = reverse_lazy('pedidos')
    success_message = "El pedido ha sido eliminado"
    permission_required = 'main_app.delete_pedido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar pedido'
        return context


@login_required(redirect_field_name='login')
@for_staff
@for_almacenero
@permission_required(('main_app.generate_billing', ))
def generar_factura(request, pk):
    p = _models.Pedido.objects.get(pk=pk)
    medicamento = _models.Medicamento.objects.get(pk=p.medicamento_id)
    t_estiba = _models.TarjetaEstiba.objects.get(
        pk=medicamento.pk)
    return render(request, 'pages/forms/pedidos_reporte.html', {'reporte': {"medicamento": medicamento.nombre, "cantidad_pagada": t_estiba.precio * p.cantidad_medicamento, "fecha": p.fecha, "no_serie": t_estiba.no_serie, "no_lote": medicamento.no_lote, "cantidad_medicamento": p.cantidad_medicamento
                                                                            }, 'title': "Reporte"})
