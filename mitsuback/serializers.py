from rest_framework import serializers
from .models import Register, WinningList

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'
    def validate(self, attrs):
        if Register.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError("Phone number already exists")
        return attrs

class WinningListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_company_name = serializers.CharField(source='user.company_name', read_only=True)
    
    class Meta:
        model = WinningList
        fields = ['id', 'user', 'user_name', 'user_company_name', 'initial', 'won_at']