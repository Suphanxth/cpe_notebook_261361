from django.contrib import admin
from app_lectures.models import Lecture

# Register your models here.

class LectureAdmin(admin.ModelAdmin):
    list_display = ['lecture_id', 'lecture_relative_url', 'notebook_id']
    search_fields = ['notebook_id']

admin.site.register(Lecture, LectureAdmin)