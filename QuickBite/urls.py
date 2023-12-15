from django.urls import path
from . import views

urlpatterns = [
    path('plot/', views.your_view, name='plot')
]
