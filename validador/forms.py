from django import forms
from django.core.validators import FileExtensionValidator as FEV



class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[FEV(['xml'], 'Utilizar apenas extensão XML', '001')],)