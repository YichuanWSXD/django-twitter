from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete

from comments.listeners import incr_comments_count, decr_comments_count
from tweets.models import Tweet
from django.contrib.contenttypes.models import ContentType
from likes.models import Like
from utils.memcached_helper import MemcachedHelper


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Sort the comments under the tweet.
        index_together = (('tweet', 'created_at'),)

    def __str__(self):
        return f'{self.created_at} - {self.user} says {self.content} at tweet {self.tweet_id}'

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Comment),
            object_id = self.id,
        ).order_by('created_at')

    @property
    def cached_user(self):
        return MemcachedHelper.get_object_through_cache(User, self.user_id)

post_save.connect(incr_comments_count, sender=Comment)
pre_delete.connect(decr_comments_count, sender=Comment)