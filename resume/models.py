from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class ResumeData(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    mobile = models.CharField(max_length=15,blank=True)
    email = models.CharField(max_length=150,blank=True)
    skills = ArrayField(models.CharField(max_length=150),blank=True)
    education = models.CharField(max_length=150,blank=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Resume Data'

class Resume(models.Model):
    resume = models.FileField(upload_to='resumes/')