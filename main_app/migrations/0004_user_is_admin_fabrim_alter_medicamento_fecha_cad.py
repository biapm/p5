# Generated by Django 4.1.3 on 2023-01-08 20:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_user_managers_alter_compra_tarjeta_bancaria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin_fabrim',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='fecha_cad',
            field=models.DateField(default=datetime.datetime(2028, 1, 7, 20, 42, 22, 279650, tzinfo=datetime.timezone.utc)),
        ),
    ]
