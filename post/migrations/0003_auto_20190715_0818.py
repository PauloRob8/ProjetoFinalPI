# Generated by Django 2.2.3 on 2019-07-15 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20190715_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='imagem',
            field=models.FileField(default=None, null=True, upload_to='media/post/'),
        ),
    ]
