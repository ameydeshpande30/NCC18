# Generated by Django 2.0.1 on 2018-02-27 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NCC', '0004_auto_20180227_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
