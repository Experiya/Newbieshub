# Generated by Django 3.1.7 on 2021-03-18 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0006_auto_20210306_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='test',
            fields=[
                ('qid', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(default='', max_length=40)),
                ('question', models.CharField(default='', max_length=500)),
                ('answer', models.CharField(default='', max_length=500)),
            ],
        ),
    ]