from __future__ import unicode_literals

from django.db import models

# Create your models here.
class symbols(models.Model):
    name = models.CharField(max_length=200) # the name of the stock/option/etf, ex: "GOOG","APPL" 
    trade_type = models.CharField(max_length = 200, default = 'stock')

    def __str__(self):
        return self.name