from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=500)
    age = models.CharField(max_length=100)
    privacy_setting = models.CharField(max_length=1000)

    def __str__(self):
        return self.description + " : " + self.name

class picture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_type = models.CharField(max_length=10)
    picture_description = models.CharField(max_length=250)
    file_path = models.CharField(max_length=700)#idk look at length later

