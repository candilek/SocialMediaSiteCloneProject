from django.contrib.auth import get_user_model #hazır user modeli import ettik
from django.contrib.auth.forms import UserCreationForm #kullnıcı-yönetici hesapları vb oluşturmak için bu formu import ettik


class UserCreateForm(UserCreationForm): #UserCreationForm referans aldık
    class Meta:
        fields = ("username", "email", "password1", "password2") #istediğimiz alanları ekledik
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
