from __future__ import unicode_literals

from django.db import models

# Create your models here.
class strategies(models.Model):
    name = models.CharField(max_length = 200)
    filename = models.CharField(max_length=256, blank=True, null=False)
    classname = models.CharField(max_length=256, blank=True, null=False)
    introduction = models.CharField(max_length=256, blank = True,null = False)
    
    def __str__(self):
        return self.name
