from django.db import models
from django.conf import settings
from django.urls import reverse
import misaka
from groups.models import Group
# Create your post models here.

from django.contrib.auth import get_user_model
User = get_user_model() #post u user olarak oturum açmış kimseye bağlamak için

class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True) #oluşturulduüğu tarih
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="posts",null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"] #en son yazılan postlar listenin en üstünde yer alacak
        unique_together = ["user", "message"] #her mesaj bir kullanıcıya bağlı oldu.
