# Generated by Django 3.1.7 on 2021-03-31 02:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_timelinec'),
        ('freelancer', '0013_timeline_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeline',
            name='name',
        ),
        migrations.CreateModel(
            name='timelineForAll',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freelancer.freelancer')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='freelancer.timelineforall')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.project')),
            ],
        ),
    ]
