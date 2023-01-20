from django.urls import path
from django.contrib.auth.views import LogoutView
from main_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # TODO: Supuesta url que debe redireccionarme para un lado o otro en caso de q el usuario sea una cosa o la otra
    path('', views.index),
    path('index', views.IndexView.as_view(), name="index"),

    path('login/', views.login_user, name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-fabrim/principal/',
         views.PrincipalTemplateView.as_view(), name='principal'),

    # TODO: Desde aqui hasta el proximo TODO es las urls del admin
    path('admin-fabrim/medicamentos/',
         views.MedicamentosView.as_view(), name='medicamentos'),
    path('admin-fabrim/medicamentos/nuevo',
         views.MedicamentosCreateView.as_view(), name='medicamentos_add'),
    path('admin-fabrim/medicamentos/delete/<int:pk>/',
         views.MedicamentoDeleteView.as_view(), name='delete_medicamento'),
    path('admin-fabrim/medicamentos/editar/<int:pk>/',
         views.MedicamentosEditView.as_view(), name='edit_medicamento'),

    path('admin-fabrim/tarjetas-estiba/',
         views.TarjetasEstibaView.as_view(), name='tarjetas-estiba'),
    path('admin-fabrim/tarjetas-estiba/nuevo',
         views.TarjetasEstibaCreateView.as_view(), name='tarjetas-estiba-add'),
    path('admin-fabrim/tarjetas-estiba/delete/<int:pk>/',
         views.TarjetaEstibaDeleteView.as_view(), name='tarjetas-estiba-delete'),
    path('admin-fabrim/tarjetas-estiba/editar/<int:pk>/',
         views.TarjetasEstibaEditView.as_view(), name='tarjetas-estiba-edit'),

    path('admin-fabrim/pedidos/',
         views.PedidosView.as_view(), name='pedidos'),
    path('admin-fabrim/pedidos/nuevo',
         views.PedidosCreateView.as_view(), name='pedidos-add'),
    path('admin-fabrim/pedidos/editar/<int:pk>/',
         views.PedidosEditView.as_view(), name='pedidos-edit'),
    path('admin-fabrim/pedidos/delete/<int:pk>/',
         views.PedidosDeleteView.as_view(), name='pedidos-delete'),
    path('admin-fabrim/pedidos/reporte/<int:pk>/',
         views.generar_factura, name='pedidos-reporte'),

    # TODO: URLs de Comprador
    path('fabrim/medicamentos/',
         views.MedicamentosListBuy.as_view(), name="index_users"),
    path("fabrim/comprar/<int:pk>/", views.comprar_medicamento, name="comprar"),
    path('fabrim/compras/', views.list_own_buys, name="compras_users"),
    path('fabrim/compras/comprobante/<int:pk>/',
         views.generar_comprobante, name="comprobante_user"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
