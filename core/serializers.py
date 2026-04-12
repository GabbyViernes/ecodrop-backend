from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SmartBin

# 1. Auth: Handles secure user registration
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}} # Keeps passwords hidden

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

# 2. Features: Transforms SmartBin data into JSON
class SmartBinSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartBin
        fields = '__all__'