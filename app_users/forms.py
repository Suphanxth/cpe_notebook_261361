from django import forms
from django.contrib.auth.forms import UserCreationForm
from app_users.models import CustomUser, Profile

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ("email",)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name")
        labels = {
            "first_name": "ชื่อ",
            "last_name": "นามสกุล"
        }

class ExtendedProfileForm(forms.ModelForm):
    prefix = "extended"
    class Meta:
        model = Profile
        fields = ("address", "phone")
        labels = {
            "address": "ที่อยู่",
            "phone": "เบอร์โทรศัพท์"
        }
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3})
        }