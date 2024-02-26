from django.shortcuts import render
from app_notebooks.models import Notebook
from django.http import HttpResponseRedirect
from django.urls import reverse
from app_general.forms import LibraryForm, LibraryModelForm
from .models import Library
from django.http import HttpRequest
from datetime import datetime, timedelta


# Create your views here.
def home(request: HttpRequest):
    request.COOKIES.get("theme")
    return render(request, 'app_general/home.html')


def about(request: HttpRequest):
    return render(request, 'app_general/about.html')


def library(request: HttpRequest):
    if request.method == 'POST':
        form = LibraryModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('library_thanks'))
    else:
        form = LibraryModelForm()
    context = {'form': form}
    return render(request, 'app_general/library_form.html', context)


def library_thanks(request: HttpRequest):
    return render(request, 'app_general/library_thanks.html')


def change_theme(request: HttpRequest):
    # referer
    referer = request.headers.get("referer")
    if referer is not None:
        response = HttpResponseRedirect(referer)
    else:
        response = HttpResponseRedirect(reverse("home"))

    response = HttpResponseRedirect(reverse("home"))
    
    # change theme
    theme = request.GET.get("theme")
    if theme == "dark":
        expired_date = datetime.now() + timedelta(days=365)
        response.set_cookie("theme", "dark", expires=expired_date, samesite="Lax")
    else:
        response.delete_cookie("theme")

    return response