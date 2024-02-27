from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    favourite_notebook_set = models.ManyToManyField(
        to="app_notebooks.Notebook", 
        through="app_users.UserFavouriteNotebook",
        related_name = "favourited_user_set"
    )

class Profile(models.Model):
    address = models.TextField(default="")
    phone = models.CharField(max_length=15, default="")
    user = models.OneToOneField("app_users.CustomUser", on_delete=models.CASCADE)

class UserFavouriteNotebook(models.Model):
    LEVELS = [
        (1, "ต้องอ่านด่วนๆ"),
        (2, "อ่านตอนว่าง"),
        (3, "บันทึกไว้ก่อน"),
    ]
    level = models.SmallIntegerField(choices=LEVELS, default=3)
    user = models.ForeignKey(
        "app_users.CustomUser", 
        on_delete=models.CASCADE,
        related_name="favourite_notebook_pivot_set"
    )
    notebook = models.ForeignKey(
        "app_notebooks.Notebook", 
        on_delete=models.CASCADE,
        related_name = "favourited_user_pivot_set"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user","notebook"],
                name="unique_user_notebook"
            )
        ]