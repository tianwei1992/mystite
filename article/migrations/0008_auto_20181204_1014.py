# Generated by Django 2.1.2 on 2018-12-04 02:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20181022_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepost',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 4, 2, 14, 55, 894848, tzinfo=utc)),
        ),
    ]
