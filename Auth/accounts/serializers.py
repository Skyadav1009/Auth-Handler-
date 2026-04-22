from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={
            'input_type': 'password'})
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {'email': {'required': True}}

    def validate_role(self, value):
        if value.lower() == 'admin':
            raise serializers.ValidationError("Admin registration is not allowed. Only one admin exists.")
        if value.lower() not in ['staff', 'employee']:
            raise serializers.ValidationError("Role does not exist. Please choose either 'staff' or 'employee'.")
        return value.lower()

    def validate_email(self, value):
        if not value.endswith('@gmail.com'):
            raise serializers.ValidationError(
                'Only @gmail.com email addresses are allowed.')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.')
        return value

    def create(self, validated_data):
        role_value = validated_data.pop('role')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'])
        
        # Create user profile with the selected role
        UserProfile.objects.create(user=user, role=role_value)
        return user


class UpdateUsernameSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={
            'input_type': 'password'})
    new_username = serializers.CharField(required=True)

    def validate_new_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'This username is already taken.')
        return value


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'date_joined')
