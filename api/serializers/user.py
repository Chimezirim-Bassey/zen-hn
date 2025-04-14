from rest_framework import serializers

from user_account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'created', 'karma', 'about', 'verified', 'avatar')
