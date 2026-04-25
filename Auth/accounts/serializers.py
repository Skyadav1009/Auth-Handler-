from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import InventorySale

User = get_user_model()

class InventorySaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventorySale
        fields = ('id', 'inventory_name', 'price', 'quantity', 'date', 'salesman')
        read_only_fields = ('salesman',)
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={
            'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role')
        extra_kwargs = {'email': {'required': True}, 'role': {'required': True}}

    def validate_role(self, value):
        role_lower = value.lower()
        if role_lower not in ['admin', 'employee', 'salesman']:
            raise serializers.ValidationError("Role does not exist. Please choose either 'admin', 'employee', or 'salesman'.")
        
        if role_lower == 'admin':
            if User.objects.filter(role='admin').exists():
                raise serializers.ValidationError("invalid email for admin")
                
        return role_lower

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'A user with this email already exists.')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username', ''),
            role=validated_data['role']
        )
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
        fields = ('email', 'username', 'role', 'date_joined')
