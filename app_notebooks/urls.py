from django.urls import path 
from . import views

urlpatterns = [
    path('', views.notebooks, name='notebooks'),
    path('<str:notebook_id>', views.notebook, name='notebook'),
    path('<str:notebook_id>/favourite', views.favourite_notebook, name='favourite_notebook'),
    path('<str:notebook_id>/unfavourite', views.unfavourite_notebook, name='unfavourite_notebook'),
    path('search/', views.search_notebooks, name='search_notebooks'),
]