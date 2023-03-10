# Generated by Django 4.1.3 on 2022-12-28 21:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compra',
            options={'ordering': ['fecha'], 'permissions': (('generate_voucher', 'can generate a voucher'),)},
        ),
        migrations.AlterModelOptions(
            name='pedido',
            options={'ordering': ['fecha'], 'permissions': (('generate_billing', 'can generate a bill'),)},
        ),
        migrations.AddField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='medicamento',
            name='fecha_cad',
            field=models.DateField(default=datetime.datetime(2027, 12, 27, 21, 17, 58, 281141, tzinfo=datetime.timezone.utc)),
        ),
    ]
