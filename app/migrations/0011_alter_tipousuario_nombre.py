# Generated by Django 4.2.4 on 2023-11-25 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_viaje_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipousuario',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]