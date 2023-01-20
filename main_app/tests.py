from django.test import TestCase, Client
from django.core.exceptions import ValidationError, FieldDoesNotExist
from django.db.utils import IntegrityError, Error
import main_app.models as _models
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class TarjetaEstibaTestCase(TestCase):

    # Configuracion inicial de los casos de prueba
    def setUp(self):
        test_user1 = get_user_model().objects.create_superuser(
            email='ar@gmail.com', name="Aarom",  apellidos="Cardenas", ci="96090512205", tfno="12345678", password='1X<ISRUkw+tuK', is_staff=True, is_customer=True, is_admin_fabrim=True)

        self.te1 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba1", precio=67, cant_medi=100)

    # Testea si el usuario esta autenticado y puede crear una tarjeta estiba
    def test_create_tarjeta_estiba_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.post(reverse(
            'tarjetas-estiba-add'), {'no_serie': 'prueba89', 'precio': 90, 'cant_medi': 90})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(
            '/admin-fabrim/tarjetas-estiba/'))

        justCreated = _models.TarjetaEstiba.objects.get(
            no_serie="prueba89")

        self.assertIsInstance(justCreated, _models.TarjetaEstiba)
        self.assertEqual(justCreated.no_serie, 'prueba89')

    # Testea si el usuario esta autenticado y puede borrar una tarjeta estiba
    def test_delete_tarjeta_estiba_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.delete(reverse(
            'tarjetas-estiba-delete', kwargs={'pk': self.te1.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(
            '/admin-fabrim/tarjetas-estiba/'))

    # Testea si el usuario esta autenticado y puede editar una tarjeta estiba
    def test_update_tarjeta_estiba_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.post(
            reverse('tarjetas-estiba-edit', kwargs={'pk': self.te1.pk}),
            {'no_serie': 'prueba00', 'precio': 90, 'cant_medi': 90})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(
            '/admin-fabrim/tarjetas-estiba/'))

        self.te1.refresh_from_db()
        self.assertEqual(self.te1.no_serie, 'prueba00')

    # Testea la creación de una tarjeta estiba con campos vacios directa a base de modelos
    # sin usuario asociado para validar campos
    def test_create_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
            _models.TarjetaEstiba.objects.create(
                no_serie=None, precio=None, cant_medi=None)

    # Testea la creación de una tarjeta estiba directamente a base de modelos
    # sin un usuarios autenticado para validar la no creación de medicamentos con el mismo no_serie
    def test_tarjeta_estiba_cant_add_and_exist_no_serie(self):
        with self.assertRaises(IntegrityError):
            _models.TarjetaEstiba.objects.create(
                no_serie="prueba1", cant_medi=100, precio=200)

    # Testea la eliminación de una tarjeta etiba no existente
    def test_delete_tarjeta_estiba_non_existing(self):
        with self.assertRaises(_models.TarjetaEstiba.DoesNotExist):
            _models.TarjetaEstiba.objects.get(id="90")


class MedicamentoTestCase(TestCase):

    # Configuracion inicial de los casos de prueba
    def setUp(self):
        test_user1 = get_user_model().objects.create_superuser(
            email='ar@gmail.com', name="Aarom",  apellidos="Cardenas", ci="96090512205", tfno="12345678", password='1X<ISRUkw+tuK', is_staff=True, is_customer=True, is_admin_fabrim=True)

        self.te1 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba1", precio=67, cant_medi=100)
        self.te2 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba2", precio=90, cant_medi=56)
        self.te3 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba3", precio=190, cant_medi=56)
        self.te4 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba4", precio=190, cant_medi=56)

        self.tm1 = _models.TipoMedicamento.objects.create(
            nombre="Antibhioticos")
        self.tm2 = _models.TipoMedicamento.objects.create(nombre="Calmantes")

        self.m1 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba11", nombre="Amocxicilina 1000g", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te1)
        self.m2 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba21", nombre="Amocxicilina 100g", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te2)
        self.m3 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba31", nombre="Amocxicilina 500g", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te3)

    # Testea si el usuario esta autenticado y puede crear un medicamento
    def test_create_medicamento_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.post(reverse(
            'medicamentos_add'), {'no_lote': 'prueba8900', 'fecha_cad': '2028-01-21', 'nombre': "Metronidazol", 'tipo_medicamento_id': str(self.tm1.pk), 'tarjeta_estiba_id': str(self.te4.pk)})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__(
            '/admin-fabrim/medicamentos/'))

        self.assertIsInstance(_models.Medicamento.objects.get(
            no_lote="prueba8900"), _models.Medicamento)
        self.assertTrue(_models.Medicamento.objects.get(
            no_lote="prueba8900"))

    # Testea si el usuario esta autenticado y puede borrar un medicamento
    def test_delete_medicamento_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.delete(reverse(
            'delete_medicamento', kwargs={'pk': self.m1.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__(
            '/admin-fabrim/medicamentos/'))

    # Testea si el usuario esta autenticado y puede editar un medicamento
    def test_update_medicamento_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.post(
            reverse('edit_medicamento', kwargs={'pk': self.m1.pk}),
            {'no_lote': 'prueba00120', 'fecha_cad': '2028-01-21', 'nombre': "Amoxicilina", 'tipo_medicamento_id': str(self.m1.tipo_medicamento_id.pk), 'tarjeta_estiba_id': str(self.m1.tarjeta_estiba_id.pk)})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__("/admin-fabrim/medicamentos/"))

        self.assertEqual(_models.Medicamento.objects.get(
            no_lote='prueba00120').no_lote, 'prueba00120')

    # Testea la creación de un medicamento con campos vacios directa a base de modelos
    # sin usuario asociado para validar campos

    def test_create_medicamento_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
            _models.Medicamento.objects.create(fecha_cad=datetime.now(
            ), no_lote=None, nombre="Amocxicilina", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te1)

    # Testea la creación de un medicamento directamente a base de modelos
    # sin un usuarios autenticado para validar la no creación de medicamentos con el mismo no_lote
    def test_medicamento_cant_add_with_same_no_lote(self):
        with self.assertRaises(IntegrityError):
            _models.Medicamento.objects.create(
                no_lote="prueba1", nombre="Amocxicilina", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te1)

    # Testea la eliminación de un medicamento no existente
    def test_delete_medicamento_non_existing(self):
        with self.assertRaises(_models.Medicamento.DoesNotExist):
            _models.Medicamento.objects.get(pk="90")


class PedidoTestCase(TestCase):

    # Configuracion inicial de los casos de prueba
    def setUp(self):
        test_user1 = get_user_model().objects.create_superuser(
            email='ar@gmail.com', name="Aarom",  apellidos="Cardenas", ci="96090512205", tfno="12345678", password='1X<ISRUkw+tuK', is_admin_fabrim=True, is_staff=True, is_customer=True,)

        self.te1 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba1", precio=67, cant_medi=100)
        self.te2 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba2", precio=90, cant_medi=56)
        self.te3 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba3", precio=190, cant_medi=56)
        self.te4 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba4", precio=190, cant_medi=56)

        self.tm1 = _models.TipoMedicamento.objects.create(
            nombre="Antibhioticos")
        self.tm2 = _models.TipoMedicamento.objects.create(nombre="Calmantes")

        self.m1 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba11", nombre="Amocxicilina 1000g", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te1)
        self.m2 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba21", nombre="Amocxicilina 100g", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te2)
        self.m3 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba31", nombre="Amocxicilina 500g", tipo_medicamento_id=self.tm1, tarjeta_estiba_id=self.te3)

        self.p1 = _models.Pedido.objects.create(
            cantidad_medicamento=90, medicamento_id=self.m1)
        self.p2 = _models.Pedido.objects.create(
            cantidad_medicamento=190, medicamento_id=self.m2)

    # Testea si el usuario esta autenticado y puede crear un pedido
    def test_create_pedido_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.post(reverse(
            'pedidos-add'), {'cantidad_medicamento': 100, 'medicamento_id': self.m1.pk})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__(
            '/admin-fabrim/pedidos/'))

        justCreated = _models.Pedido.objects.get(
            id=3)

        self.assertIsInstance(justCreated, _models.Pedido)
        self.assertEqual(justCreated.cantidad_medicamento, 100)

    # Testea si el usuario esta autenticado y puede borrar un medicamento
    def test_delete_pedido_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.delete(reverse(
            'pedidos-delete', kwargs={'pk': self.p1.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__(
            '/admin-fabrim/pedidos/'))

    # Testea si el usuario esta autenticado y puede editar un pedido
    def test_update_pedido_by_form(self):
        login = self.client.login(
            username='ar@gmail.com', password='1X<ISRUkw+tuK')

        response = self.client.post(
            reverse('pedidos-edit', kwargs={'pk': self.p2.pk}),
            {'cantidad_medicamento': 250, 'medicamento_id': self.m2.pk})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__(
            '/admin-fabrim/pedidos/'))

        self.p2.refresh_from_db()
        self.assertEqual(self.p2.cantidad_medicamento, 250)

    # Testea la creación de un pedido con campos vacios directa a base de modelos
    # sin usuario asociado para validar campos
    def test_create_pedido_with_empty_fields(self):
        with self.assertRaises(IntegrityError):
            _models.Pedido.objects.create(
                medicamento_id=self.m2, cantidad_medicamento=None)

    # Testea la eliminación de un medicamento no existente
    def test_delete_pedido_non_existing(self):
        with self.assertRaises(_models.Pedido.DoesNotExist):
            _models.Pedido.objects.get(pk="90")


class UserModelTest(TestCase):

    # Chequea la creacion correcta de un usuario en la base de datos con todos los campos
    def test_create_user_with_email_successful(self):
        """Comprueba q el usuario tenga un email"""
        email = "test@example.com"
        name = "Pepe"
        apellidos = "Perez"
        ci = '96090512205'
        tfno = '53211465'
        password = "12345678"

        user = get_user_model().objects.create_user(
            email,
            name,
            apellidos,
            ci,
            tfno,
            password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    # Chequea la normalizacion del correo, que no es mas que en caso de
    # que el usuario escriba el correo con mayusculas lo lleve todo a
    # minusculas antes de guardarlo en base de datos
    def test_new_user_email_normalized(self):
        """Normaliza el email"""
        email = "test@EXAMPLE.COM"
        user = get_user_model().objects.create_user(
            email,
            name="Pepe",
            ci='96090512205',
            tfno='53211465',
            password="password",
            apellidos="Perez",
        )

        self.assertEqual(user.email, email.lower())

    # Chequea la creacion invalida de un usuario en la base de datos con el campo correo
    # vacio y el servidor responde un ValueError existosamente ante el caso de prueba
    def test_new_user_invalid_email(self):
        """Chackea q halla un email valido"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                name="Pepe",
                ci='96090512205',
                tfno='53211465',
                password="password",
                apellidos="Perez",
            )

    # Testea la creacion de un superusuario en base de datos y q los campos is_superuser
    # e is_staff esten en True al finalizar la creación
    def test_create_new_superuser(self):
        """Checkque si los datos del superusuario son validos"""

        email = "test@example.com"
        name = "Pepe"
        apellidos = "Perez"
        ci = '96090512205'
        tfno = '53211465'
        password = "12345678"

        user = get_user_model().objects.create_superuser(
            email,
            name,
            apellidos,
            ci,
            tfno,
            password,
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class CompraTestCase(TestCase):

    def setUp(self):
        test_user1 = get_user_model().objects.create_user(
            email='bpm@uci.cu', name="Beatriz",  apellidos="Pérez", ci="99072812205", tfno="12345678", password='1X<ISRUkw+tuK', is_customer=True)

        permission_view_medicamento = Permission.objects.get(
            codename="view_medicamento").id
        permission_add_compra = Permission.objects.get(
            codename="add_compra").id
        permission_view_medicamento = Permission.objects.get(
            codename="generate_voucher").id

        test_user1.user_permissions.add(permission_view_medicamento)
        test_user1.user_permissions.add(permission_add_compra)
        test_user1.user_permissions.add(permission_view_medicamento)
        test_user1.save()

        self.te1 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba1", precio=67, cant_medi=100)
        self.te2 = _models.TarjetaEstiba.objects.create(
            no_serie="prueba2", precio=80, cant_medi=100)

        self.tm1 = _models.TipoMedicamento.objects.create(nombre="Vitamina")

        self.m1 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba01", nombre="Vitamina C", tarjeta_estiba_id=self.te1,  tipo_medicamento_id=self.tm1)
        self.m2 = _models.Medicamento.objects.create(fecha_cad=datetime.now(
        ), no_lote="prueba02", nombre="Vitamina B12", tarjeta_estiba_id=self.te2,  tipo_medicamento_id=self.tm1)

    # Testea si se puede realizar la compra de un medicamento y esta se registra en la
    # base de datos, asi como la modificacion de la tarjeta estiba asociada al cambiar la cantidad de medicamentos
    def test_comprar_medicamento(self):
        login = self.client.login(
            username='bpm@uci.cu', password='1X<ISRUkw+tuK')

        response = self.client.post(
            reverse('comprar', kwargs={'pk': self.m1.pk}),
            {'tarjeta_bancaria': '9224069991023520', 'cantidad': '3'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.__eq__(
            '/fabrim/medicamentos/'))

        self.assertEqual(_models.Compra.objects.get(
            tarjeta_bancaria="9224069991023520").medicamento_id.tarjeta_estiba_id.cant_medi, 97)
        self.assertIsInstance(_models.Compra.objects.get(
            tarjeta_bancaria="9224069991023520"), _models.Compra)
