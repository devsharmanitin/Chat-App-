# Generated by Django 4.2.4 on 2023-09-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ExThree', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
