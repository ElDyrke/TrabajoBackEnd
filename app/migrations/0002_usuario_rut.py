# Generated by Django 4.2.7 on 2023-11-18 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='rut',
            field=models.CharField(default=11111110, max_length=10),
            preserve_default=False,
        ),
    ]
