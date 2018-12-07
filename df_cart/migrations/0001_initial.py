# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0002_auto_20180921_1508'),
        ('df_goods', '0002_auto_20180926_0946'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('count', models.IntegerField(default=0)),
                ('goods', models.ForeignKey(to='df_goods.GoodsInfo')),
                ('user', models.ForeignKey(to='df_user.UserInfo')),
            ],
        ),
    ]
