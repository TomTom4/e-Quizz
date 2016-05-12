# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-12 13:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Quizz', '0004_remove_lost_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='lost',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 12, 13, 51, 49, 922104, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
