from django import forms
from .models import  Message_User


class UploadFileForm(forms.Form):
    file=forms.FileField()