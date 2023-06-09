# import xml.etree.ElementTree as ET
from lxml import etree as ET
from django.shortcuts import render
import validador.rulesXML as rules
from .forms import UploadFileForm
from datetime import datetime
import re

def validadorxml(request, infor):
    return render(request, "validador/validadorxml.html", infor)


def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES["file"]
            errors = []
            for message in rules.validate_schema(f):
                errors.append(message)
            f.seek(0)
            file = ET.parse(f)
            root = file.getroot()

            nsNFE = {
                'ns': "http://www.portalfiscal.inf.br/nfe"
            }
            caminho = rules.best_way(file)

            modelo_nfe = root.find(caminho + 'ns:ide/ns:mod', nsNFE)
            # VALIDAÇÃO DO TIPO DE NOTA FISCAL
            infor = rules.type_nota(file, caminho, modelo_nfe)
            infor['metodo'] = request.method
            infor['form'] = form
            infor['errors'] = errors
            return render(request, "validador/validadorxml.html", infor)
    else:
        form = UploadFileForm()
    return render(request, "validador/index.html", {"form": form, "metodo": request.method})
