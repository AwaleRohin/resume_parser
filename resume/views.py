from django.shortcuts import render, redirect
from django.conf import settings
from resume import forms
from resume import models
from resume.common import extract_data
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector


def upload_resume(request):
    if request.method == 'POST':
        try:
            form = forms.ResumeUploadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                url = settings.BASE_DIR + '/resume/media/resumes/' + \
                    request.FILES['resume'].name
                extract_data.extract_text(url)
                return redirect('list')
        except Exception as e:
            print(e)
    else:
        form = forms.ResumeUploadForm()
    return render(request, 'home.html', {'form': form})


def lists(request):
    resume_data = models.ResumeData.objects.all()
    return render(request, 'list.html', {'data': resume_data})


def filter_resume(request):
    vector = SearchVector('skills')
    query = SearchQuery(request.GET['search'].strip())
    data = models.ResumeData.objects.annotate(
        rank=SearchRank(vector, query)).order_by('-rank')
    print(data)
    return render(request, 'list.html', {'data': data})
