from rest_framework import serializers
from .models import supplier

class supplier1(serializers.ModelSerializer):
    class Meta:
        model= supplier
        fields = '__all__'