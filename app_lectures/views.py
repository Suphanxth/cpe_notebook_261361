from django.shortcuts import render
from app_notebooks.models import Notebook
from django.http import HttpResponseRedirect
from django.urls import reverse
from app_general.forms import LibraryForm, LibraryModelForm
from app_lectures.models import Lecture
from .models import Lecture
from django.shortcuts import render, get_object_or_404

# Create your views here.
def lectures(request):
    all_lectures = Lecture.objects.order_by('lecture_id')
    context = {'lectures': all_lectures}
    return render(request, 'app_lectures/lectures.html', context)

def lecture(request, lecture_id):
    lecture = get_object_or_404(Lecture, lecture_id=lecture_id)
    return render(request, 'app_lectures/lectures.html', {'lecture': lecture})