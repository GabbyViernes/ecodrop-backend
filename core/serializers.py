from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SmartBin, MaintenanceAlert, DepositLog

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class SmartBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBin
        fields = '__all__'

class MaintenanceAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceAlert
        fields = '__all__'

class DepositLogSerializer(serializers.ModelSerializer):
    # These helpers make it easier for the React table to display names
    user_display = serializers.ReadOnlyField(source='user.username')
    bin_display = serializers.ReadOnlyField(source='smart_bin.bin_id')

    class Meta:
        model = DepositLog
        fields = [
            'id', 'user', 'user_display', 'smart_bin', 
            'bin_display', 'material', 'weight_kg', 
            'reward_points', 'timestamp'
        ]