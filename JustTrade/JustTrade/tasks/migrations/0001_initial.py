# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('symbols', '0001_initial'),
        ('strategies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tradeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trade_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='tradingTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('real_time_index', models.BooleanField(default=True)),
                ('waitingtime', models.CharField(default='30', max_length=200)),
                ('trade_config_json', models.TextField(null=True, blank=True)),
                ('strategy', models.ForeignKey(to='strategies.strategies')),
                ('symbol', models.ForeignKey(to='symbols.symbols')),
            ],
        ),
        migrations.AddField(
            model_name='tradelog',
            name='trade_task',
            field=models.ForeignKey(related_name='logs', to='tasks.tradingTask'),
        ),
    ]
