from rest_framework import serializers
from .models import tradingTask, tradeLog

class tradingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = tradingTask
        fields = {'is_active','waitingtime','symbol','strategy','trade_config_json'}


class tradeLogSerializer(serializers.ModelSerializer):
	class Meta:
		model = tradeLog
		fields = {'trade_type','trade_time'}