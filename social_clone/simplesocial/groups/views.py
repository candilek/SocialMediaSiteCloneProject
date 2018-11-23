from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(LoginRequiredMixin,PermissionRequiredMixin)
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group,GroupMember
from . import models

class CreateGroup(LoginRequiredMixin, generic.CreateView):#user login durumda olmalı
    fields = ("name", "description")
    model = Group #group modelini bağladık

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try: #grup üyeri nesnesini oluşturduk- kiliği doğrulanmış user sınıfından
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:#hata durumunda(büütülük hatası -?)
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs): #kullanıcının yanlışlıkla başka bir gruptan ayrılmaması için
        try:
            membership = models.GroupMember.objects.filter( #nesneleri filtreledik
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()
#üyelik oluşturucaz.useer ve diğer üyerin de o grupta olduğunu varsayıyoruz.Daha sonra "bu grupta değilsin" uyarısı verilsin
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,"You can't leave this group because you aren't in it.")

        else:
            membership.delete()  #üyeliğin silinmesi işlemi
            messages.success(self.request,"You have successfully left this group.")
        return super().get(request, *args, **kwargs)
