from django import forms
from .models import *


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["name", "thumb"]
