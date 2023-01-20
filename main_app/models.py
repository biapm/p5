from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import Group

ci_regex = RegexValidator(
    '^\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{5}$', 'Carnet de identidad invalido')
tfno_regex = RegexValidator('^\+53\d{8}$', 'Telefono invalido')

apto_regex = RegexValidator(
    '^([0-1][0-5]?[0-9]|\d{2})[1-3][0-1][0-9]$', 'Apartamento UCI invalido')

tb_regex = RegexValidator(
    '^(9224|9225|9200|9235)(9598|1299|0699)\d{8}$', "Tarjeta bancaria invalida")

nombre_regex = RegexValidator(
    '^[A-Za-záéíóú]{3,}(\s[A-Za-záéíóú]{3,})?$', "El nombre solo admite letras y al menos 3 caracteres")

apellidos_regex = RegexValidator(
    '^[A-Za-záéíóú]{3,}(\s[A-Za-záéíóú]{3,})?$', "El/Los apellido(s) solo admite(n) letras y al menos 3 caracteres")


class OwnUserManager(BaseUserManager):
    """Manager para usuarios"""
    use_in_migrations = True

    def create_user(self, email, name, apellidos,  ci, tfno, password=None, **extra_kwargs):
        """Crea un nuevo Usuario"""
        if not email:
            raise ValueError("El usuario debe tener un email")

        user = self.model(email=self.normalize_email(email), name=name,
                          apellidos=apellidos, ci=ci, tfno=tfno, **extra_kwargs)

        user.is_customer = True
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, name, apellidos,  ci, tfno, password=None, **extra_kwargs):
        user = self.create_user(email, name, apellidos, ci, tfno,
                                password, **extra_kwargs)

        user.is_superuser = True
        user.is_staff = True
        user.is_customer = False

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Modelo BD para Users"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, validators=[nombre_regex])
    apellidos = models.CharField(max_length=255, validators=[apellidos_regex])
    ci = models.CharField(max_length=11, unique=True,
                          null=False, blank=False, validators=[ci_regex])
    tfno = models.CharField(max_length=50, validators=[tfno_regex])
    apto = models.CharField(max_length=50, validators=[apto_regex])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin_fabrim = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    objects = OwnUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'apellidos', 'ci', 'tfno']

    def get_full_name(self):
        return "%s %s" % (self.name, self.apellidos)

    def get_short_name(self):
        return self.name

    def __str__(self):
        """Return String"""
        return "%s %s - %s" % (self.name, self.apellidos, self.email)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @ property
    def if_staff(self):
        return self.is_staff


class TipoMedicamento(models.Model):
    nombre = models.CharField(
        max_length=255, unique=True, null=False, blank=False)

    def __str__(self):
        """Return String"""
        return self.nombre


class TarjetaEstiba(models.Model):
    no_serie = models.CharField(
        max_length=255, unique=True, null=False, blank=False)
    precio = models.IntegerField(blank=False, null=False)
    cant_medi = models.IntegerField(blank=False, null=False)
    fecha_creacion = models.DateField(blank=False, null=False, auto_now=True)

    class Meta:
        ordering = ['no_serie', 'fecha_creacion']

    def __str__(self):
        return "%s %s %s %s" % (self.no_serie, self.precio, self.cant_medi, self.fecha_creacion)


class Medicamento(models.Model):
    nombre = models.CharField(max_length=255, blank=False, null=False)
    no_lote = models.CharField(
        max_length=255, unique=True, null=False, blank=False)
    fecha_cad = models.DateField(blank=False, null=False, default=(
        timezone.now() + timedelta(days=1825)))
    tarjeta_estiba_id = models.OneToOneField(
        TarjetaEstiba, on_delete=models.CASCADE, primary_key=True)
    tipo_medicamento_id = models.ForeignKey(
        TipoMedicamento, on_delete=models.CASCADE)

    class Meta:
        ordering = ['fecha_cad', 'no_lote', 'nombre']

    def __str__(self):
        return "%s - %s - %s" % (self.nombre, self.no_lote, self.fecha_cad)


class Pedido(models.Model):
    cantidad_medicamento = models.IntegerField(blank=False, null=False)
    fecha = models.DateField(blank=False, null=False, auto_now=True)
    medicamento_id = models.ForeignKey(
        Medicamento, on_delete=models.CASCADE)

    class Meta:
        ordering = ['fecha']
        permissions = (("generate_billing", "can generate a bill"),)

    def __str__(self):
        return "%s %s" % (self.medicamento_id.nombre, self.fecha)


class Compra(models.Model):
    fecha = models.DateField(blank=False, null=False, auto_now=True)
    tarjeta_bancaria = models.CharField(
        max_length=255, null=False, blank=False, validators=[tb_regex])
    cantidad = models.IntegerField(blank=False, null=False, default=1, validators=[MaxValueValidator(3, "La cantidad debe ser menor o igual a 3"),
                                                                                   MinValueValidator(1, "La cantidad al menos debe ser 1")])
    total_pagado = models.IntegerField(blank=False, null=False)
    medicamento_id = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['fecha']
        permissions = (("generate_voucher", "can generate a voucher"),)

    def __str__(self):
        return "%s %s" % (self.tarjeta_bancaria, self.medicamento_id.nombre)
