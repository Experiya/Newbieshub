# Generated by Django 3.1.7 on 2021-03-18 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancer', '0007_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='q1',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='test',
            name='q2',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='test',
            name='q3',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='test',
            name='q4',
            field=models.CharField(default='', max_length=500),
        ),
    ]
