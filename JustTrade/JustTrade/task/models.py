from __future__ import unicode_literals

from django.db import models
from symbols.model import symbols
from strategy.model import strategies
from django.utils import timezone
# Create your models here.
class tradingTask(models.Model):
	is_active = models.BooleanField(default=True)
	waitingtime = models.IntegerField(blank=False, null=False)  # number of seconds.
	symbol = models.ForeignKey(symbols,blank = False)
	strategy = models.ForeignKey(strategies,blank = False)


	trade_config_json = models.TextField(blank=True, null=True)


class tradeLog(models.Model):
	trade_type = models.ForeignKey(tradingTask,blank = False)
	alert_time = models.DateTimeField(default=timezone.now, null=True)