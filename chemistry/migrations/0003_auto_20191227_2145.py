# Generated by Django 2.2.7 on 2019-12-27 21:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('chemistry', '0002_auto_20191227_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acid',
            name='when_added',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 21, 45, 39, 967026, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='hydroxide',
            name='when_added',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 27, 21, 45, 39, 982576, tzinfo=utc)),
        ),
    ]
