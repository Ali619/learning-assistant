from rest_framework import serializers

from apps.chat.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']


class ChatSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)
    plugin_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False)
    user_message = serializers.CharField(required=True)
