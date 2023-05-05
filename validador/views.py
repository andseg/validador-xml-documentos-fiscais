import xml.etree.ElementTree as ET
from django.shortcuts import render
from validador.rulesXML import validator_rules
from .forms import UploadFileForm


def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = ET.parse(request.FILES["file"])
            root = file.getroot()
            xml = ET.tostring(root, encoding='unicode', method='xml')
            nsNFE = {
                'ns': "http://www.portalfiscal.inf.br/nfe"
            }
            schema = root.find('ns:NFe/ns:infNFe/ns:ide/ns:mod', nsNFE)
            if schema is not None:
                caminho = 'ns:NFe/ns:infNFe/'
            else:
                caminho = 'ns:infNFe/'

            modelo_nfe = root.find(caminho + 'ns:ide/ns:mod', nsNFE)

            serie_nfe = root.find(caminho + 'ns:ide/ns:serie', nsNFE)
            numero_nfe = root.find(caminho + 'ns:ide/ns:nNF', nsNFE)

            dest_nfe = root.find(caminho + 'ns:dest/ns:xNome', nsNFE)
            emitente_nfe = root.find(caminho + 'ns:emit/ns:xNome', nsNFE)

            cnpj_emit_nfe = root.find(caminho + 'ns:emit/ns:CNPJ', nsNFE)
            cnpj_dest_nfe = root.find(caminho + 'ns:dest/ns:CNPJ', nsNFE)

            # Para fins de validação
            emit_uf = root.find(caminho + 'ns:emit/ns:enderEmit/ns:UF', nsNFE)
            det_uf = root.find(caminho + 'ns:dest/ns:enderDest/ns:UF', nsNFE)
            lista_alq_produto = []
            for det in root.findall(caminho + 'ns:det', nsNFE):
                alq_icms_nfe = det.find('ns:imposto/ns:ICMS/ns:ICMS20/ns:pICMS', nsNFE)
                if alq_icms_nfe is not None:
                    lista_alq_produto.append(alq_icms_nfe.text)
                else:
                    alq_icms_nfe = '0'
                    lista_alq_produto.append(alq_icms_nfe)

            chave_nfe = root.find('ns:NFe/ns:infNFe', nsNFE)
            chave_nfe = chave_nfe.attrib['Id'][3:]
            cnpj_emit_nfe_format = '{}.{}.{}/{}-{}'.format(cnpj_emit_nfe.text[:2], cnpj_emit_nfe.text[2:5],
                                                           cnpj_emit_nfe.text[5:8], cnpj_emit_nfe.text[8:12],
                                                           cnpj_emit_nfe.text[12:])
            cnpj_dest_nfe_format = '{}.{}.{}/{}-{}'.format(cnpj_dest_nfe.text[:2], cnpj_dest_nfe.text[2:5],
                                                           cnpj_dest_nfe.text[5:8], cnpj_dest_nfe.text[8:12],
                                                           cnpj_dest_nfe.text[12:])

            produtos = []

            for det in root.findall(caminho + 'ns:det', nsNFE):
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
            alq_validado = validator_rules(emit_uf.text, det_uf.text, lista_alq_produto)
            print(alq_validado)
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
                'xml': xml,
                'modelo': modelo_nfe,
                'alq_validado': alq_validado
            }

            return render(request, "validador/index.html", infor)
    else:
        form = UploadFileForm()
    return render(request, "validador/index.html", {"form": form, "metodo": request.method})
