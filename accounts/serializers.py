from rest_framework import serializers
from .models import UserProfile, Inventory

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UpdateUsernameSerializer(serializers.Serializer):
    new_username = serializers.CharField(max_length=150)

class DeleteAccountSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()

class UserProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address', 'age', 'gender', 'profile_picture', 'user_type')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = UserProfile(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class SellerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address', 'age', 'gender', 'profile_picture')

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
            age=validated_data.get('age'),
            gender=validated_data.get('gender'),
            profile_picture=validated_data.get('profile_picture'),
            user_type=\'seller\'
        )
        return user

class StaffRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'phone_number', 'address', 'age', 'gender', 'profile_picture')

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
            age=validated_data.get('age'),
            gender=validated_data.get('gender'),
            profile_picture=validated_data.get('profile_picture'),
            user_type=\'staff\',
            is_staff=True
        )
        return user

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'name', 'price', 'quantity')
