# Generated by Django 2.2.7 on 2019-12-27 21:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chemistry', '0004_auto_20191227_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='container',
            name='Plot',
        ),
        migrations.AlterField(
            model_name='acid',
            name='when_added',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 21, 48, 44, 475989, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hydroxide',
            name='when_added',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 21, 48, 44, 492167, tzinfo=utc)),
        ),
    ]
