from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save

from accounts.listeners import profile_changed
from utils.listeners import invalidate_object_cache


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    avatar = models.FileField(null=True)

    nickname = models.CharField(null=True, max_length=200)
    created_at = models .DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.nickname)

def get_profile(user):
    from accounts.services import UserService
    if hasattr(user, '_cached_user_profile'):
        return getattr(user, '_cached_user_profile')
    profile = UserService.get_profile_through_cache(user.id)
    # profile, _ = UserProfile.objects.get_or_create(user=user)
    setattr(user, '_cached_user_profile', profile)
    return profile

# Add profile property to User Model
User.profile = property(get_profile)


# hook up with listeners to invalidate caches
# pre_delete.connect(user_changed, sender=User)
# post_save.connect(user_changed, sender=User)
pre_delete.connect(invalidate_object_cache, sender=User)
pre_delete.connect(invalidate_object_cache, sender=User)

pre_delete.connect(profile_changed, sender=UserProfile)
post_save.connect(profile_changed, sender=UserProfile)