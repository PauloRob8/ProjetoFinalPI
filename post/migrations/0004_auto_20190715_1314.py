# Generated by Django 2.2.3 on 2019-07-15 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20190715_0818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='conteudo',
            field=models.CharField(max_length=50),
        ),
    ]
