# Generated by Django 2.2.3 on 2019-07-15 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfis', '0007_perfil_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='foto_perfil',
            field=models.FileField(default=None, null=True, upload_to='media/perfis/'),
        ),
    ]
