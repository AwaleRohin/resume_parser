from django.shortcuts import render, redirect
from django.conf import settings
from resume import forms
from resume import models
from resume.common import extract_data


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
    return render(request , 'list.html', {'data':resume_data})
