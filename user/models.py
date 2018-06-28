from django.db import models
from django.urls import reverse

# Create your models here.
class Friend(models.Model):
    name = models.CharField(max_length=250)
    user_title = models.CharField(max_length=500)
    user_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.user_title + " - " + self.name

class Pic(models.Model):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    pic_name = models.CharField(max_length=250)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.pic_name + "." + self.file_type

    def get_absolute_url(self):
        return reverse('user:details', kwargs={'pk': self.friend.pk})