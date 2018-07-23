from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



PRIVACY_LEVELS = (
    ('0', 'Just Me'),
    ('1', 'Friends'),
    ('2', 'Everyone'),
)

# Create your models here.
class Prof(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    privacy_level = models.CharField(max_length=1, choices=PRIVACY_LEVELS)
    bio = models.CharField(max_length=500)
    profile_picture = models.FileField()

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.user.pk})

    def __str__(self):
        return "username: " + self.user.username + " email: " \
               + self.user.email

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Prof.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_prof(sender, instance, **kwargs):
        instance.prof.save()


class Pic(models.Model):
    prof = models.ForeignKey(Prof, on_delete=models.CASCADE)
    pic_desc = models.CharField(max_length=10)
    pic_name = models.CharField(max_length=250)
    pic_publicity = models.CharField(max_length=1, choices=PRIVACY_LEVELS)
    picture = models.FileField()

    def __str__(self):
        return self.pic_name + "." + self.file_type

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.prof.pk})


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE, null=True)

    @classmethod
    def makeFriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)
        # new_friend.friend.users.add(current_user)

    @classmethod
    def removeFriend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)
        # new_friend.friend.users.remove(current_user)

    # @classmethod
    # def friendList:
    #     return Null