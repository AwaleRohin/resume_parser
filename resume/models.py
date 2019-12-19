from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.dispatch import receiver
import os
from django.core.validators import FileExtensionValidator

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
    resume = models.FileField(upload_to='resumes/',validators=[FileExtensionValidator(['pdf', 'doc' ])])


@receiver(models.signals.post_delete, sender=Resume)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    try:
        if sender.__name__== 'Resume':
            if instance.resume:
                print(instance.resume.path)
                if os.path.isfile(instance.resume.path):
                    os.remove(instance.resume.path)
    except Exception as e:
        print('Delete on change',e)
        pass

