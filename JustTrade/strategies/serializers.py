from rest_framework import serializers
from .models import strategies

class strategiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = strategies
        fields = {'name','filename','classname'}