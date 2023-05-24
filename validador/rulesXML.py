import pathlib
import pandas as pd
import xml.dom.minidom
from lxml import etree as ET
import re
from datetime import datetime

WORKING_DIR = str(pathlib.Path().resolve())
SCRIPT_DIR = str(pathlib.Path(__file__).parent.resolve())


def walks_xml(file, caminho):
    root = file.getroot()
    nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}
    lista_de_tags = []
    for tag in root.findall(caminho, nsNFE):
        nome_tag = tag.tag.split('}')[1]
        nome_tag_sem_namespace = nome_tag.replace('{http://www.portalfiscal.inf.br/nfe}', '')
        dados_tag = ET.tostring(tag, encoding='utf-8').decode('utf-8')
        tags = {'tag': f'<{nome_tag_sem_namespace}>{dados_tag}</{nome_tag_sem_namespace}>'}
        lista_de_tags.append(tags)
    for item in lista_de_tags:
        tag_formatada = item['tag'].replace('{http://www.portalfiscal.inf.br/nfe}', '')
        dom = xml.dom.minidom.parseString(tag_formatada)
        xml_formatado = dom.toprettyxml(indent='  ')


def validator_rules(origin, dest, mod, vnf, alq_nfe, valor_tribt):
    alq_icms = pd.read_excel("./validador/aliquotas/aliquotaICMS.xlsx", index_col=0)
    alq = alq_icms.loc[origin, dest]
    if mod == '55':
        for aliquota in alq_nfe:
            if float(aliquota.replace(" ' ", "")) != 0:
                if float(aliquota.replace(" ' ", "")) == alq:
                    alq_validado = 'Alíquota ICMS Correta ' + origin + '-' + dest + ' Alíquota: ' + str(alq) + '%'
                    return alq_validado
                else:
                    alq_validado = 'Alíquota ICMS utilizado:' + aliquota + '%' + '  Origem: ' + origin + '  Destino: ' + dest + ' O correto seria: ' + str(
                        alq) + '%'
                    return alq_validado
            else:

                alq_validado = 'Inconsistência Encontrada não existe pICMS no arquivo'
                return alq_validado

    else:
        alq_icms = pd.read_excel("./validador/aliquotas/aliquotaICMS.xlsx", index_col=0)
        alq = alq_icms.loc[origin, origin]
        for aliquota in alq_nfe:
            if float(aliquota.replace(" ' ", "")) != 0:
                if float(aliquota.replace(" ' ", "")) == alq:
                    alq_validado = 'Alíquota ICMS Correta ' + origin + ' Alíquota: ' + str(alq) + '%'
                    return alq_validado
                else:
                    alq_validado = 'Alíquota ICMS utilizado:' + aliquota + '%' + '  Origem: ' + origin + '  Destino: ' + dest + ' o correto seria: ' + str(
                        alq) + '%'
                    return alq_validado
            else:
                valor_icms = (alq / 100) * vnf
                if valor_icms == valor_tribt:
                    alq_validado = 'ICMS - Ok'
                    return alq_validado
                else:
                    alq_validado = 'Encontrado inconsistência no ICMS'
                    return alq_validado


def rules_recebimentos(vpag, vnf):
    valor_total = sum(vpag)
    if valor_total != vnf:
        diferenca = valor_total - vnf
        retorno = ('vPag Erro   ' + 'Valor Total = R$' + str(vnf) + '   Valor Pago = R$' + str(
            valor_total) + '    Diferença = R$' + str(diferenca))
        return retorno
    else:
        retorno = 'vPag - OK'
        return retorno


def best_way(file):
    root = file.getroot()
    nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}
    schema = root.find('ns:NFe/ns:infNFe/ns:ide/ns:mod', nsNFE)
    if schema is not None:
        caminho = 'ns:NFe/ns:infNFe/'
    else:
        caminho = 'ns:infNFe/'
    return caminho


def operacao_mov(file, caminho):
    root = file.getroot()
    nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}
    tipo_operacao = root.find(caminho + 'ns:ide/ns:natOp', nsNFE)
    return tipo_operacao.text


def tipo_nota(file, caminho, modelo_nfe):
    if modelo_nfe.text == '55':
        root = file.getroot()
        nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}
        xml = ET.tostring(root, encoding='UTF-8', method='xml')
        serie_nfe = root.find(caminho + 'ns:ide/ns:serie', nsNFE)
        numero_nfe = root.find(caminho + 'ns:ide/ns:nNF', nsNFE)

        dest_nfe = root.find(caminho + 'ns:dest/ns:xNome', nsNFE)
        emitente_nfe = root.find(caminho + 'ns:emit/ns:xNome', nsNFE)

        cnpj_emit_nfe = root.find(caminho + 'ns:emit/ns:CNPJ', nsNFE)
        cnpj_dest_nfe = root.find(caminho + 'ns:dest/ns:CNPJ', nsNFE)
        data_emi = root.find(caminho + 'ns:ide/ns:dhEmi', nsNFE)
        data_objeto = datetime.fromisoformat(data_emi.text)
        data_formatada = data_objeto.strftime("%d-%m-%Y %H:%M")
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
                alq_icms_nfe = det.find('ns:imposto/ns:ICMS/ns:ICMS00/ns:pICMS', nsNFE)
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
        valor_total = root.find(caminho + 'ns:total/ns:ICMSTot/ns:vNF', nsNFE)
        valor_tribut = root.find(caminho + 'ns:total/ns:ICMSTot/ns:vTotTrib', nsNFE)
        alq_validado = validator_rules(emit_uf.text, det_uf.text, modelo_nfe.text, float(valor_total.text),
                                       lista_alq_produto, float(valor_tribut.text))
        recebimento = []

        for pag in root.findall(caminho + 'ns:pag/ns:detPag', nsNFE):
            pagamento = pag.find('ns:vPag', nsNFE)
            recebimento.append(float(pagamento.text))
        erro_pagamento = rules_recebimentos(recebimento, float(valor_total.text))
        xml_sem_namespace = re.sub(b'ns0:', b'', xml)
        xml_sem_namespace_format = xml_sem_namespace.decode('utf-8')
        infor = {
            'Serie': serie_nfe.text,
            'Numero_da_Nota': numero_nfe.text,
            'Emitente': emitente_nfe.text,
            'CNPJ_Emitente': cnpj_emit_nfe_format,
            'Destinatario': dest_nfe.text,
            'CNPJ_Destinatario': cnpj_dest_nfe_format,
            'Chave_de_Acesso': chave_nfc,
            'produtos': produtos,
            'xml': xml_sem_namespace_format,
            'modelo': modelo_nfe.text,
            'alq_validado': alq_validado,
            'erro_pagamento': erro_pagamento,
            'data': data_formatada
        }
        return infor


    elif modelo_nfe.text == '65':
        root = file.getroot()
        nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}
        xml = ET.tostring(root, encoding='UTF-8', method='xml')
        serie_nfc = root.find(caminho + 'ns:ide/ns:serie', nsNFE)
        numero_nfc = root.find(caminho + 'ns:ide/ns:nNF', nsNFE)

        emitente_nfc = root.find(caminho + 'ns:emit/ns:xNome', nsNFE)

        cnpj_emit_nfc = root.find(caminho + 'ns:emit/ns:CNPJ', nsNFE)

        # Para fins de validação
        emit_uf = root.find(caminho + 'ns:emit/ns:enderEmit/ns:UF', nsNFE)
        data_emi = root.find(caminho + 'ns:ide/ns:dhEmi', nsNFE)
        data_objeto = datetime.fromisoformat(data_emi.text)
        data_formatada = data_objeto.strftime("%d-%m-%Y %H:%M")
        lista_alq_produto_nfc = []
        for det in root.findall(caminho + 'ns:det', nsNFE):
            alq_icms_nfc = det.find('ns:imposto/ns:ICMS/ns:ICMS20/ns:pICMS', nsNFE)
            if alq_icms_nfc is not None:
                lista_alq_produto_nfc.append(alq_icms_nfc.text)
            else:
                alq_icms_nfe = det.find('ns:imposto/ns:ICMS/ns:ICMS00/ns:pICMS', nsNFE)
                if alq_icms_nfe is not None:
                    lista_alq_produto_nfc.append(alq_icms_nfe.text)
                else:
                    # vTotTrib * 100 / vNf = Aliquota ICMS
                    # total_tributos = det.find('ns:total/ns:ICMSTot/ns:vTotTrib', nsNFE)
                    # alq_icms_nfe = (float(total_tributos.text) * 100) / float(valor_total.text)
                    alq_icms_nfe = '0'
                    lista_alq_produto_nfc.append(alq_icms_nfe)

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
            qtd_prod_format = float(qtd_prod_nfc.text)
            produto = {
                'codigo': codigo_prod_nfc.text,
                'nome': nome_prod_nfc.text,
                'valor_unitario': item_prod_format,
                'quantidade': qtd_prod_format,
                'valor_total': valor_prod_nfc.text
            }
            produtos.append(produto)

        valor_total = root.find(caminho + 'ns:total/ns:ICMSTot/ns:vNF', nsNFE)
        recebimento = []
        for pag in root.findall(caminho + 'ns:pag/ns:detPag', nsNFE):
            pagamento = pag.find('ns:vPag', nsNFE)
            recebimento.append(float(pagamento.text))
        erro_pagamento = rules_recebimentos(recebimento, float(valor_total.text))
        valor_tribut = root.find(caminho + 'ns:total/ns:ICMSTot/ns:vTotTrib', nsNFE)
        alq_validado = validator_rules(emit_uf.text, emit_uf.text, modelo_nfe.text, float(valor_total.text),
                                       lista_alq_produto_nfc, float(valor_tribut.text))
        xml_sem_namespace = re.sub(b'ns0:', b'', xml)
        xml_sem_namespace_format = xml_sem_namespace.decode('utf-8')

        infor = {
            'Serie': serie_nfc.text,
            'Numero_da_Nota': numero_nfc.text,
            'Emitente': emitente_nfc.text,
            'CNPJ_Emitente': cnpj_emit_nfc_format,
            'Chave_de_Acesso': chave_nfc,
            'produtos': produtos,
            'xml': xml_sem_namespace_format,
            'modelo': modelo_nfe.text,
            'alq_validado': alq_validado,
            'erro_pagamento': erro_pagamento,
            'data': data_formatada
        }
        return infor
    
    
def validate_schema(file):
    try:
        file.seek(0)
        schema_path = '/schemas/'
        xml = ET.parse(file)
        xml_root = xml.getroot()
        
        if xml_root.tag.__contains__('consReciNFe'):
            schema_path += 'consReciNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('consSitNFe'):
            schema_path += 'consSitNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('consStatServ'):
            schema_path += 'consStatServ_v4.00.xsd'
        elif xml_root.tag.__contains__('enviNFe'):
            schema_path += 'enviNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('inutNFe'):
            schema_path += 'inutNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('NFe'):
            schema_path += 'nfe_v4.00.xsd'
        elif xml_root.tag.__contains__('ProcInutNFe'):
            schema_path += 'procInutNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('nfeProc'):
            schema_path += 'procNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('retConsReciNFe'):
            schema_path += 'retConsReciNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('retConsSitNFe'):
            schema_path += 'retConsSitNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('retConsStatServ'):
            schema_path += 'retConsStatServ_v4.00.xsd'
        elif xml_root.tag.__contains__('retEnviNFe'):
            schema_path += 'retEnviNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('retInutNFe'):
            schema_path += 'retInutNFe_v4.00.xsd'
        elif xml_root.tag.__contains__('Signature'):
            schema_path += 'xmldsig-core-schema_v1.01.xsd'
        else:
            raise ET.DocumentInvalid('Schema não identificado. Verificar se o XML é referente a um documento fiscal')
        
        xml_schema = ET.XMLSchema(file=SCRIPT_DIR + schema_path)
        xml_schema.assertValid(xml)
        return ['Schema validado com sucesso!']
    
    except Exception as e:
        errors = []
        for error in e.error_log:
            errors.append(prettify_error(error))
        return errors
    
    
def prettify_error(error: ET._LogEntry):
    error_message = error.message
    line = str(error.line)
    element = error_message[error_message.find('}')+1:]
    element = element[:element.find("'")]
    message = error_message[error_message.find(':',error_message.find('}')+1)+2:]
    return 'Elemento: ' + element + '\nMensagem: ' + message + '\nLinha: ' + line
    
        
    
