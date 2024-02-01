from django.urls import path
from . import views

urlpatterns = [
    path('', views.lectures, name='lectures'),
    path('<str:lecture_id>/', views.lecture, name='lecture')
]