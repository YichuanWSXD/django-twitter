from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from inbox.api.serializers import NotificationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class NotificationViewSet(
    viewsets.GenericViewSet,
    viewsets.mixins.ListModelMixin,
)

    serializer_class = NotificationSerializer
    permission_class = (IsAuthenticated,)
    filterset_fields = ('unread',)

    def get_queryset(self):
        return self.request.notification.all()

    @action(method=['GET'], detail=False, url_path='unread-count')
    def unread_count(self, request, *args, **kwargs):
        count = self.get_queryset().filter(unread=True).count()
        return Response({'unread_count': count}, status=status.HTTP_200_OK)

    @action(method=['POST'], detail=False, url_path='market-all-as-read')
    def mark_all_as_read(self, request, *args, **kwargs):
        updated_count = self.get_queryset().update(unread=False)
        return Response({'marketd_count': updated_count}, status=status.HTTP_200_OK)