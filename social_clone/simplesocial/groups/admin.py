from django.contrib import admin
from . import models

# Register your models here.
class GroupMemberInline(admin.TabularInline):#Grup üyelerini düzenleyebilmek için
    model = models.GroupMember #rup üyeleri sıralamak için

admin.site.register(models.Group)
