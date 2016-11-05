from rest_framework import serializers
from .models import symbols

class symbolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = symbols
        fields = {'name','trade_type'}