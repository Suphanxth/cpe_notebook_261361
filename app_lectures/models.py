from django.db import models
from app_notebooks.models import Notebook

# Create your models here.
class Lecture(models.Model):
    lecture_id = models.CharField(max_length=100, null=True, blank=True)
    lecture_relative_url = models.CharField(max_length=100, null=True, blank=True)
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='lectures')

    def __str__(self) -> str:
        return '{} {}'.format(self.lecture_id, self.notebook)
