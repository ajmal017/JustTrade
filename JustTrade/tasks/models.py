from __future__ import unicode_literals

from django.db import models
from symbols.models import symbols
from strategies.models import strategies
from django.utils import timezone
# Create your models here.


class tradingTask(models.Model):
    is_active = models.BooleanField(default=True)
    real_time_index = models.BooleanField(default=True)
    waitingtime = models.CharField(max_length=200, default='30')  # number of seconds.
    symbol = models.ForeignKey(symbols, blank=False)
    strategy = models.ForeignKey(strategies, blank=False)

    trade_config_json = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.pk)


class tradeLog(models.Model):
    trade_task = models.ForeignKey(tradingTask, blank=False, on_delete=models.CASCADE, related_name='logs')
    log_time = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=100)
    log_info = models.CharField(max_length=100)

    def __unicode__(self):
        return str(self.pk)
