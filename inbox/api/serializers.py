from django.contrib.auth.models import User
from rest_framework import serializers
from notifications.models import Notification
from accounts.api.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer()
    def get_recipient(self, instance):
        return UserSerializer(
            MemcachedHelper.get_object_through_cache(User, instance.actor_object_id)
        )
    class Meta:
        model = Notification
        fields =(
            'id',
            'recipient',
            'actor_content_type',
            'actor_object_id',
            'verb',
            'action_object_content_type',
            'action_object_object_id',
            'target_content_type',
            'target_object_id',
            'timestamp',
            'unread',
        )

class NotificationSerializerForUpdate(serializers.ModelSerializer):
    unread = serializers.BooleanField

    class Meta:
        model = Notification
        fields = ('unread',)

    def update(self, instance, validated_data):
        instance.unread = validated_data['unread']
        instance.save()
        return instance