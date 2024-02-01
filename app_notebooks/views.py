from django.http.response import HttpResponse
from django.shortcuts import render
from .models import Notebook

# Create your views here.
def notebooks(request):
    all_notebooks = Notebook.objects.order_by('code')
    context = {'notebooks': all_notebooks}
    return render(request, 'app_notebooks/notebooks.html', context)

def notebook(request, notebook_id):
    one_notebook = None
    try:
        one_notebook = Notebook.objects.get(id=notebook_id)
    except:
        print('ไม่พบรายวิชานี้')
    context = { 'notebook': one_notebook }
    return render(request, 'app_notebooks/notebook.html', context)