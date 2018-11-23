from django.db import models
from django.contrib import auth
from django.utils import timezone

# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):#User sınıfını referans alıcaz

    def __str__(self):
        return "@{}".format(self.username) #User sınıfından gelen özellikler otomatik form oluşturmak için kullandık
