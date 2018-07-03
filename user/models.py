from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Prof(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    friend_title = models.CharField(max_length=500)
    friend_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.friend_title + " - " + self.name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Prof.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_prof(sender, instance, **kwargs):
        instance.prof.save()

class Pic(models.Model):
    friend = models.ForeignKey(Prof, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    pic_name = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.pic_name + "." + self.file_type

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.friend.pk})