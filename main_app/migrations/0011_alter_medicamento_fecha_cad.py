# Generated by Django 4.1.3 on 2023-01-20 00:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_medicamento_fecha_cad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamento',
            name='fecha_cad',
            field=models.DateField(default=datetime.datetime(2028, 1, 19, 0, 38, 35, 718606, tzinfo=datetime.timezone.utc)),
        ),
    ]
