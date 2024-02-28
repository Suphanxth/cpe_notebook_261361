from django.http.response import HttpResponse
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from .models import Notebook
from app_notebooks.forms import FavouriteNotebookForm
from django.contrib.auth.decorators import login_required
from app_users.models import UserFavouriteNotebook
from django.urls import reverse


# Create your views here.
def notebooks(request):
    all_notebooks = Notebook.objects.order_by('code')
    context = {'notebooks': all_notebooks}
    return render(request, 'app_notebooks/notebooks.html', context)


def notebook(request: HttpRequest, notebook_id):
    one_notebook = None
    is_favourite_notebook = False
    try:
        one_notebook = Notebook.objects.get(id=notebook_id)
        if request.user.is_authenticated:
            user_favourite_notebook = UserFavouriteNotebook.objects.get(
                user=request.user,
                notebook=one_notebook
            )
            is_favourite_notebook = user_favourite_notebook is not None
    except:
        print('ไม่พบรายวิชานี้')
    form = FavouriteNotebookForm()
    context = { 
        'notebook': one_notebook, 
        "form": form,
        "is_favourite_notebook": is_favourite_notebook,
    }
    return render(request, 'app_notebooks/notebook.html', context)


@login_required
def favourite_notebook(request: HttpRequest, notebook_id):
    if request.method == "POST":
        form = FavouriteNotebookForm(request.POST)
        if form.is_valid():
            # user_favourite_notebook: UserFavouriteNotebook = form.save(commit=False)
            # user_favourite_notebook.user = request.user
            # user_favourite_notebook.notebook = Notebook(id=notebook_id)
            # user_favourite_notebook.save()
            UserFavouriteNotebook.objects.update_or_create(
                defaults={"level": form.cleaned_data.get("level")},
                user=request.user,
                notebook=Notebook(id=notebook_id),
            )
    return HttpResponseRedirect(request.headers.get("referer"))


@login_required
def unfavourite_notebook(request: HttpRequest, notebook_id):
    if request.method == 'POST':
        request.user.favourite_notebook_set.remove(Notebook(id=notebook_id))
    return HttpResponseRedirect(reverse("dashboard"))