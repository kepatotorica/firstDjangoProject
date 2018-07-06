from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Prof(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=250)
    bio = models.CharField(max_length=500)
    profile_picture = models.FileField()

    #return str([f.name for f in self.user._meta.get_fields()])
    #feilds in user include, found using the command above
    # ['prof',
    #  'logentry',
    #  'id',
    #  'password',
    #  'last_login',
    #  'is_superuser',
    #  'username',
    #  'first_name',
    #  'last_name',
    #  'email',
    #  'is_staff',
    #  'is_active',
    #  'date_joined',
    #  'groups',
     # 'user_permissions']

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.user.pk})

    def __str__(self):
        return "username: " + self.user.username + " email :"\
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
    file_type = models.CharField(max_length=10)
    pic_name = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)
    profile_picture = models.FileField()

    def __str__(self):
        return self.pic_name + "." + self.file_type

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.prof.pk})