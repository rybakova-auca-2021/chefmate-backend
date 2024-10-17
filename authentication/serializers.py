from rest_framework import serializers
from django.utils import timezone
from .models import (
    User
)


class BaseRegisterSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()

    class Meta:
        model = User

    def get_message(self, obj):
        return (
            "Verification message has been sent to your phone number, please verify your phone!"
        )

    def create(self, validated_data):
        return User.objects.create_user( **validated_data)


class RegisterWithEmailSerializer(BaseRegisterSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(BaseRegisterSerializer.Meta):
        fields = ["email", "password", "confirm_password"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"required": True},
            "confirm_password": {"required": True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return super().create(validated_data)


class RegisterUserSerializer(BaseRegisterSerializer):
    class Meta(BaseRegisterSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "phone",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "phone": {"required": True},
        }


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


    class Meta:
        fields = [
            "email",
            "password",
        ]


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields = [
            "email",
        ]

class PasswordSetSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

class SendCodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=4)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "profile_photo", 
        ]

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)

        instance.save()
        return instance

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
