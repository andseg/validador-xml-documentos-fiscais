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
            rules.validate_schema(request.FILES["file"])
            # file = ET.parse(request.FILES["file"])
            # root = file.getroot()

            # nsNFE = {
            #     'ns': "http://www.portalfiscal.inf.br/nfe"
            # }
            # caminho = rules.best_way(file)

            # modelo_nfe = root.find(caminho + 'ns:ide/ns:mod', nsNFE)
            # VALIDAÇÃO DO TIPO DE NOTA FISCAL
            # infor = rules.tipo_nota(xml, modelo_nfe=modelo)
            infor = {}
            infor['metodo'] = request.method
            infor['form'] = form
            return render(request, "validador/validadorxml.html", infor)
    else:
        form = UploadFileForm()
    return render(request, "validador/index.html", {"form": form, "metodo": request.method})
