import xml.etree.ElementTree as ET
from django.shortcuts import render
from validador.rulesXML import validator_rules, validador_rules_nfce
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
            # VALIDAÇÃO DO TIPO DE NOTA FISCAL
            if modelo_nfe.text == '55':
                serie_nfe = root.find(caminho + 'ns:ide/ns:serie', nsNFE)
                numero_nfe = root.find(caminho + 'ns:ide/ns:nNF', nsNFE)

                dest_nfe = root.find(caminho + 'ns:dest/ns:xNome', nsNFE)
                emitente_nfe = root.find(caminho + 'ns:emit/ns:xNome', nsNFE)

                cnpj_emit_nfe = root.find(caminho + 'ns:emit/ns:CNPJ', nsNFE)
                cnpj_dest_nfe = root.find(caminho + 'ns:dest/ns:CNPJ', nsNFE)
                fisico = False
                if cnpj_dest_nfe is None:
                    fisico = True
                    cnpj_dest_nfe = root.find(caminho + 'ns:dest/ns:CPF', nsNFE)

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

                chave_nfc = root.find('ns:infNFe', nsNFE)
                if chave_nfc is None:
                    chave_nfc = root.find('ns:NFe/ns:infNFe', nsNFE).attrib['Id'][3:]
                else:
                    chave_nfc = chave_nfc.attrib['Id'][3:]

                cnpj_emit_nfe_format = '{}.{}.{}/{}-{}'.format(cnpj_emit_nfe.text[:2], cnpj_emit_nfe.text[2:5],
                                                               cnpj_emit_nfe.text[5:8], cnpj_emit_nfe.text[8:12],
                                                               cnpj_emit_nfe.text[12:])

                if not fisico:
                    cnpj_dest_nfe_format = '{}.{}.{}/{}-{}'.format(cnpj_dest_nfe.text[:2], cnpj_dest_nfe.text[2:5],
                                                                   cnpj_dest_nfe.text[5:8], cnpj_dest_nfe.text[8:12],
                                                                   cnpj_dest_nfe.text[12:])
                else:
                    cnpj_dest_nfe_format = '{}.{}.{}-{}'.format(cnpj_dest_nfe.text[:3], cnpj_dest_nfe.text[3:5],
                                                                cnpj_dest_nfe.text[5:8], cnpj_dest_nfe.text[11:])

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
                    'Chave_de_Acesso': chave_nfc,
                    'produtos': produtos,
                    'xml': xml,
                    'modelo': modelo_nfe.text,
                    'alq_validado': alq_validado
                }
                return render(request, "validador/index.html", infor)

            elif modelo_nfe.text == '65':
                serie_nfc = root.find(caminho + 'ns:ide/ns:serie', nsNFE)
                numero_nfc = root.find(caminho + 'ns:ide/ns:nNF', nsNFE)

                emitente_nfc = root.find(caminho + 'ns:emit/ns:xNome', nsNFE)

                cnpj_emit_nfc = root.find(caminho + 'ns:emit/ns:CNPJ', nsNFE)

                # Para fins de validação
                emit_uf = root.find(caminho + 'ns:emit/ns:enderEmit/ns:UF', nsNFE)
                lista_alq_produto_nfc = []
                for det in root.findall(caminho + 'ns:det', nsNFE):
                    alq_icms_nfc = det.find('ns:imposto/ns:ICMS/ns:ICMS20/ns:pICMS', nsNFE)
                    if alq_icms_nfc is not None:
                        lista_alq_produto_nfc.append(alq_icms_nfc.text)
                    else:
                        alq_icms_nfc = '0'
                        lista_alq_produto_nfc.append(alq_icms_nfc)

                chave_nfc = root.find('ns:infNFe', nsNFE)
                if chave_nfc is None:
                    chave_nfc = root.find('ns:NFe/ns:infNFe', nsNFE).attrib['Id'][3:]
                else:
                    chave_nfc = chave_nfc.attrib['Id'][3:]

                cnpj_emit_nfc_format = '{}.{}.{}/{}-{}'.format(cnpj_emit_nfc.text[:2], cnpj_emit_nfc.text[2:5],
                                                               cnpj_emit_nfc.text[5:8], cnpj_emit_nfc.text[8:12],
                                                               cnpj_emit_nfc.text[12:])
                produtos = []

                for det in root.findall(caminho + 'ns:det', nsNFE):
                    nome_prod_nfc = det.find('ns:prod/ns:xProd', nsNFE)
                    item_prod_nfc = det.find('ns:prod/ns:vUnCom', nsNFE)
                    item_prod_format = round(float(item_prod_nfc.text), 2)
                    codigo_prod_nfc = det.find('ns:prod/ns:cProd', nsNFE)
                    valor_prod_nfc = det.find('ns:prod/ns:vProd', nsNFE)
                    qtd_prod_nfc = det.find('ns:prod/ns:qCom', nsNFE)
                    qtd_prod_format = round(float(qtd_prod_nfc.text))
                    produto = {
                        'codigo': codigo_prod_nfc.text,
                        'nome': nome_prod_nfc.text,
                        'valor_unitario': item_prod_format,
                        'quantidade': qtd_prod_format,
                        'valor_total': valor_prod_nfc.text,
                    }
                    produtos.append(produto)
                alq_validado = validador_rules_nfce(emit_uf.text, lista_alq_produto_nfc)
                print(alq_validado)
                infor = {
                    'metodo': request.method,
                    'form': form,
                    'Serie': serie_nfc.text,
                    'Numero_da_Nota': numero_nfc.text,
                    'Emitente': emitente_nfc.text,
                    'CNPJ_Emitente': cnpj_emit_nfc_format,
                    'Chave_de_Acesso': chave_nfc,
                    'produtos': produtos,
                    'xml': xml,
                    'modelo': modelo_nfe.text,
                    'alq_validado': alq_validado
                }
                return render(request, "validador/index.html", infor)
    else:
        form = UploadFileForm()
    return render(request, "validador/index.html", {"form": form, "metodo": request.method})
