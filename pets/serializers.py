from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Pet, AdoptionRequest


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    # Create a new user
    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email") # Email is optional
        )
        user.set_password(validated_data["password"]) # Hash the password
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            'id', 'name', 'age', 'species', 'city',
            'photo', 'photo_url', 'status', 'description', 'owner'
        ]
        read_only_fields = ['owner']

class AdoptionRequestSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)

    class Meta:
        model = AdoptionRequest
        fields = ['id', 'pet', 'requester_name', 'phone', 'email', 'message', 'created_at']
        read_only_fields = ['created_at']

class AdoptionRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdoptionRequest
        fields = ['pet', 'requester_name', 'phone', 'email', 'message']