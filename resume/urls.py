from django.urls import path
from . import views as resume_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    path('',resume_views.upload_resume, name='upload'),
    path('list',resume_views.lists, name='list'),
    path('search',resume_views.filter_resume, name='search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
