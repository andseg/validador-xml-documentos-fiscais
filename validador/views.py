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
            # xml_as_string = handler.handle_uploaded_file(request.FILES["file"])
            # file = request.FILES["file"].read().decode('utf-8')
            file = ET.parse(request.FILES["file"])
            root = file.getroot()
            xml = ET.tostring(root, encoding='unicode', method='xml')

            nsNFE = {
                'ns': "http://www.portalfiscal.inf.br/nfe"
            }
            serie_nfe = root.find('ns:NFe/ns:infNFe/ns:ide/ns:serie', nsNFE)
            numero_nfe = root.find('ns:NFe/ns:infNFe/ns:ide/ns:nNF', nsNFE)
            emitente_nfe = root.find('ns:NFe/ns:infNFe/ns:emit/ns:xNome', nsNFE)
            cnpj_emit_nfe = root.find('ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFE)
            cnpj_dest_nfe = root.find('ns:NFe/ns:infNFe/ns:dest/ns:CNPJ', nsNFE)
            dest_nfe = root.find('ns:NFe/ns:infNFe/ns:dest/ns:xNome', nsNFE)
            chave_nfe = root.find('ns:NFe/ns:infNFe', nsNFE)
            chave_nfe = chave_nfe.attrib['Id'][3:]
            cnpj_emit_nfe_format = '{}.{}.{}/{}-{}'.format(cnpj_emit_nfe.text[:2], cnpj_emit_nfe.text[2:5],
                                                           cnpj_emit_nfe.text[5:8], cnpj_emit_nfe.text[8:12],
                                                           cnpj_emit_nfe.text[12:])
            cnpj_dest_nfe_format = '{}.{}.{}/{}-{}'.format(cnpj_dest_nfe.text[:2], cnpj_dest_nfe.text[2:5],
                                                           cnpj_dest_nfe.text[5:8], cnpj_dest_nfe.text[8:12],
                                                           cnpj_dest_nfe.text[12:])

            produtos = []

            for det in root.findall('ns:NFe/ns:infNFe/ns:det', nsNFE):
                nome_prod_nfe = det.find('ns:prod/ns:xProd', nsNFE)
                item_prod_nfe = det.find('ns:prod/ns:vUnCom', nsNFE)
                item_prod_format = round(float(item_prod_nfe.text), 2)
                codigo_prod_nfe = det.find('ns:prod/ns:cProd', nsNFE)
                valor_prod_nfe = det.find('ns:prod/ns:vProd', nsNFE)
                qtd_prod_nfe = det.find('ns:prod/ns:qCom', nsNFE)
                qtd_prod_format = round(float(qtd_prod_nfe.text))
                produto = {
                    'codigo': codigo_prod_nfe.text,
                    'nome': nome_prod_nfe.text,
                    'valor_unitario': item_prod_format,
                    'quantidade': qtd_prod_format,
                    'valor_total': valor_prod_nfe.text,
                }
                produtos.append(produto)

            infor = {
                'metodo': request.method,
                'form': form,
                'Serie': serie_nfe.text,
                'Numero_da_Nota': numero_nfe.text,
                'Emitente': emitente_nfe.text,
                'CNPJ_Emitente': cnpj_emit_nfe_format,
                'Destinatario': dest_nfe.text,
                'CNPJ_Destinatario': cnpj_dest_nfe_format,
                'Chave_de_Acesso': chave_nfe,
                'produtos': produtos,
                'xml': xml
            }

            return render(request, "validador/index.html", infor)
    else:
        form = UploadFileForm()
    return render(request, "validador/index.html", {"form": form, "metodo": request.method})
