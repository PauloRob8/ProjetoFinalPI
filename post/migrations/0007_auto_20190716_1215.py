# Generated by Django 2.2.3 on 2019-07-16 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_post_marcacoes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='marcacoes',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
