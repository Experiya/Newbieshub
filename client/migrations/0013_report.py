# Generated by Django 3.1.7 on 2021-04-01 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_auto_20210331_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='report',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('freelancer', models.CharField(default='', max_length=40)),
                ('client', models.CharField(default='', max_length=40)),
                ('flag', models.CharField(default='', max_length=40)),
            ],
        ),
    ]
