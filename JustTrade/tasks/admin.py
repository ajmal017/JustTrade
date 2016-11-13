from django.contrib import admin

from .models import tradingTask, tradeLog

# Register your models here.


class tradeLogAdmin(admin.ModelAdmin):
	list_display = ['trade_task', 'log_type', 'log_info']
	readonly_fields = ('trade_time',)

admin.site.register(tradingTask)
admin.site.register(tradeLog, tradeLogAdmin)
