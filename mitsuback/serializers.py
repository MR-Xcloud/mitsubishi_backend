from rest_framework import serializers
from .models import Register, WinningList

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'

class WinningListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = WinningList
        fields = ['id', 'user', 'user_name', 'user_email', 'initial', 'won_at']