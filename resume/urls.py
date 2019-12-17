from django.urls import path
from . import views as resume_views

urlpatterns =[
    path('',resume_views.home)
]
