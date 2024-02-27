from django import forms
from app_users.models import UserFavouriteNotebook

class FavouriteNotebookForm(forms.ModelForm):
    class Meta:
        model = UserFavouriteNotebook
        fields = ["level"]
        widgets = {
            "level": forms.RadioSelect
        }