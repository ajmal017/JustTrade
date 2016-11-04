from django.contrib import admin

from .models import tradingTask,tradeLog

# Register your models here.

admin.site.register(tradingTask)
admin.site.register(tradeLog)