from django.db import models

# Create your models here.
class Switch(models.Model):
    feature_name = models.CharField(max_length=100)
    toggle = models.BooleanField(default=False)
    feature_desc = models.TextField()

    def __str__(self):
        return "{feature_name} ==> {toggle}".format(feature_name=self.feature_name, toggle = self.toggle)
