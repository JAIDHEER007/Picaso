from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Image(models.Model):
    img_uid = models.CharField(max_length=11)
    img_prompt = models.TextField()
    creation_date = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.img_uid

class JoinTable(models.Model):
    img = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



            
