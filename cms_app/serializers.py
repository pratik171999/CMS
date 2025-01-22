from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from cms_app.models import ContentItem

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'phone', 'address', 'city', 'state', 'country', 'pincode','is_admin']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ContentItemSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')  # Adjust if necessary

    class Meta:
        model = ContentItem
        fields = ['title', 'body', 'summary', 'document', 'author', 'categories']