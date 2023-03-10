# Generated by Django 4.1.3 on 2023-01-11 02:31

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_user_is_admin_fabrim_alter_medicamento_fecha_cad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='fecha_cad',
            field=models.DateField(default=datetime.datetime(2028, 1, 10, 2, 31, 56, 351258, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='apellidos',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[A-Za-záéíóú]{3,}(\\s[A-Za-záéíóú]{3,})?$', 'El/Los apellido(s) solo admite(n) letras y al menos 3 caracteres')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[A-Za-záéíóú]{3,}(\\s[A-Za-záéíóú]{3,})?$', 'El nombre solo admite letras y al menos 3 caracteres')]),
        ),
    ]
