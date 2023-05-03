import xml.etree.ElementTree as ET
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils import encoding
from .forms import UploadFileForm
from . import handler


def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            xml_as_string = handler.handle_uploaded_file(request.FILES["file"])
            xml = ET.fromstring(xml_as_string)
            
            return render(request, 
                          "validador/index.html", 
                          {'form': form, "file": xml_as_string})
            
            
            
    else:
        form = UploadFileForm()
    return render(request, "validador/index.html", {"form": form})


