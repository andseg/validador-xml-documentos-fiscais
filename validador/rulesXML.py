import pathlib
import pandas as pd
from lxml import etree as ET
import re
from datetime import datetime

WORKING_DIR = str(pathlib.Path().resolve())
SCRIPT_DIR = str(pathlib.Path(__file__).parent.resolve())


def validator_rules_55(origin, dest, alq_nfe, valor_tribt):
    alq_icms = pd.read_excel("./validador/aliquotas/aliquotaICMS.xlsx", index_col=0)
    alq = alq_icms.loc[origin, dest]
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

def validator_rules_65(origin, vnf, alq_nfe, valor_tribt):
        alq_icms = pd.read_excel("./validador/aliquotas/aliquotaICMS.xlsx", index_col=0)
        alq = alq_icms.loc[origin, origin]
        for aliquota in alq_nfe:
            if float(aliquota.replace(" ' ", "")) != 0:
                if float(aliquota.replace(" ' ", "")) == alq:
                    alq_validado = 'Alíquota ICMS Correta ' + origin + ' Alíquota: ' + str(alq) + '%'
                    return alq_validado
                else:
                    alq_validado = 'Alíquota ICMS utilizado:' + aliquota + '%' + '  Origem: ' + origin + '  Destino: ' + origin + ' o correto seria: ' + str(
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

def rules_receipts(vpag, vnf):
    valor_total = sum(vpag)
    if valor_total != vnf:
        diferenca = valor_total - vnf
        retorno = ('Encontrado Erro quanto a Informação de Pagamento   ' + 'Valor Total = R$' + str(
            vnf) + '   Valor Pago = R$' + str(
            valor_total) + '    Diferença = R$' + str(diferenca))
        return retorno
    else:
        retorno = 'Informação de Pagamento - OK'
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


def operation_mov(file, caminho):
    root = file.getroot()
    nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}
    tipo_operacao = root.find(caminho + 'ns:ide/ns:natOp', nsNFE)
    return tipo_operacao.text


def inform_tributos(file, caminho):
    root = file.getroot()
    nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}
    infCpl = root.find(caminho + 'ns:infAdic/ns:infCpl', nsNFE)
    if infCpl is None:
        infCpl = ''
    else:
        infCpl = infCpl.text
    return infCpl


def format_cnpj(cnpj):
    cnpj_format = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5],
                                          cnpj[5:8], cnpj[8:12],
                                          cnpj[12:])
    return cnpj_format


def format_cpf(cpf):
    cpf_format = '{}.{}.{}-{}'.format(cpf[:3],  cpf[3:6],
                                      cpf[6:9], cpf[9:])
    return cpf_format


def cnpj_cpf(root, caminho, nsNFE):
    cnpj_dest = root.find(caminho + 'ns:dest/ns:CNPJ', nsNFE)
    if cnpj_dest is not None:
        dest_name = root.find(caminho + 'ns:dest/ns:xNome', nsNFE)
        cnpj_dest_format = format_cnpj(cnpj_dest.text)
        cpf_dest_format = None
        return dest_name.text, cnpj_dest_format, cpf_dest_format

    else:
        cpf_dest = root.find(caminho + 'ns:dest/ns:CPF', nsNFE)
        if cpf_dest is not None:
            dest_name = root.find(caminho + 'ns:dest/ns:xNome', nsNFE)
            cpf_dest_format = format_cpf(cpf_dest.text)
            cnpj_dest_format = None
            return dest_name.text, cnpj_dest_format, cpf_dest_format
        else:
            dest_name = 'Consumidor Final'
            cpf_dest_format = '000.000.000-00'
            cnpj_dest_format = None
            return dest_name, cnpj_dest_format, cpf_dest_format


def local_emit(root, caminho, nsNFE):
    emit_uf = root.find(caminho + 'ns:emit/ns:enderEmit/ns:UF', nsNFE)
    return emit_uf


def local_dest(root, caminho, nsNFE):
    dest_uf = root.find(caminho + 'ns:dest/ns:enderDest/ns:UF', nsNFE)
    return dest_uf


def type_nota(file, caminho, modelo_nfe):
    root = file.getroot()
    nsNFE = {'ns': "http://www.portalfiscal.inf.br/nfe"}

    # Validação de Informações Comuns entre os arquivos
    xml = ET.tostring(root, encoding='UTF-8', method='xml')
    serie = root.find(caminho + 'ns:ide/ns:serie', nsNFE)
    numero = root.find(caminho + 'ns:ide/ns:nNF', nsNFE)
    emitente = root.find(caminho + 'ns:emit/ns:xNome', nsNFE)
    if emitente is None:
        emitente = ''
    else:
        emitente = emitente.text
    
    cnpj_emit = root.find(caminho + 'ns:emit/ns:CNPJ', nsNFE)
    if cnpj_emit is None:
        cnpj_emit = ''
    else:
        cnpj_emit = cnpj_emit.text
    
    cnpj_emit_format = format_cnpj(cnpj_emit)

    # Encontrando Estado do Emitente

    emit_uf = local_emit(root, caminho, nsNFE)

    # Validação do Tipo de Cliente (Pode existir ou Não) caso None retorna genérico
    dest_name, cnpj_dest, cpf_dest = cnpj_cpf(root, caminho, nsNFE)
    if cnpj_dest is not None:
        dest_uf = local_dest(root, caminho, nsNFE)
    else:
        dest_uf = None

    # Informação Comun para validar data
    data_emi = root.find(caminho + 'ns:ide/ns:dhEmi', nsNFE)
    data_objeto = datetime.fromisoformat(data_emi.text)
    data_formatada = data_objeto.strftime("%d-%m-%Y %H:%M")

    # Validando as informações de Alíquota ICMS
    lista_alq_produto = []
    for det in root.findall(caminho + 'ns:det', nsNFE):
        alq_icms = det.find('ns:imposto/ns:ICMS/ns:ICMS20/ns:pICMS', nsNFE)
        if alq_icms is not None:
            lista_alq_produto.append(alq_icms.text)
        else:
            alq_icms = det.find('ns:imposto/ns:ICMS/ns:ICMS00/ns:pICMS', nsNFE)
            if alq_icms is not None:
                lista_alq_produto.append(alq_icms.text)
            else:
                # vTotTrib * 100 / vNf = Aliquota ICMS
                # total_tributos = det.find('ns:total/ns:ICMSTot/ns:vTotTrib', nsNFE)
                # alq_icms = (float(total_tributos.text) * 100) / float(valor_total.text)
                alq_icms = '0'
                lista_alq_produto.append(alq_icms)

    # Buscando a chave de acesso
    chave_acesso = root.find('ns:infNFe', nsNFE)
    if chave_acesso is None:
        chave_acesso = root.find('ns:NFe/ns:infNFe', nsNFE).attrib['Id'][3:]
    else:
        chave_acesso = chave_acesso.attrib['Id'][3:]

    # Percorrendo e inserindo me lista os produtos da nota
    produtos = []
    for det in root.findall(caminho + 'ns:det', nsNFE):
        nome_prod = det.find('ns:prod/ns:xProd', nsNFE)
        item_prod = det.find('ns:prod/ns:vUnCom', nsNFE)
        item_prod_format = round(float(item_prod.text), 2)
        codigo_prod = det.find('ns:prod/ns:cProd', nsNFE)
        valor_prod = det.find('ns:prod/ns:vProd', nsNFE)
        qtd_prod = det.find('ns:prod/ns:qCom', nsNFE)
        qtd_prod_format = float(qtd_prod.text)
        produto = {
            'codigo': codigo_prod.text,
            'nome': nome_prod.text,
            'valor_unitario': item_prod_format,
            'quantidade': qtd_prod_format,
            'valor_total': valor_prod.text
        }
        produtos.append(produto)

    # Percorrendo e armazenando as informações de Pagamento disponíveis
    valor_total = root.find(caminho + 'ns:total/ns:ICMSTot/ns:vNF', nsNFE)
    recebimento = []
    for pag in root.findall(caminho + 'ns:pag/ns:detPag', nsNFE):
        pagamento = pag.find('ns:vPag', nsNFE)
        recebimento.append(float(pagamento.text))

    # Inserção de Regras
    erro_pagamento = rules_receipts(recebimento, float(valor_total.text))
    xml_sem_namespace = re.sub(b'ns0:', b'', xml)
    xml_sem_namespace_format = xml_sem_namespace.decode('utf-8')

    # Inicio de informações Fiscais
    op = operation_mov(file, caminho)
    infcpl = inform_tributos(file, caminho)
    
    valor_tribut = root.find(caminho + 'ns:total/ns:ICMSTot/ns:vTotTrib', nsNFE)
    
    if dest_uf is not None:
        if valor_tribut is not None:
            alq_validado = validator_rules_55(emit_uf.text, dest_uf.text,
                                           lista_alq_produto, float(valor_tribut.text))
        else:
            valor_tribut = 0
            alq_validado = validator_rules_55(emit_uf.text, dest_uf.text,
                                              lista_alq_produto, float(valor_tribut))
    else:
        alq_validado = validator_rules_65(emit_uf.text, float(valor_total.text),
                                       lista_alq_produto, float(valor_tribut.text))

    if modelo_nfe.text == '65':
        infor = {
            'Serie': serie.text,
            'Numero_da_Nota': numero.text,
            'Emitente': emitente,
            'Chave_de_Acesso': chave_acesso,
            'CNPJ_Emitente': cnpj_emit_format,
            'op': op,
            'infcpl': infcpl,
            'produtos': produtos,
            'xml': xml_sem_namespace_format,
            'modelo': modelo_nfe.text,
            'alq_validado': alq_validado,
            'erro_pagamento': erro_pagamento,
            'data': data_formatada
        }
        if cnpj_dest is not None:
            infor['cnpj_cpf_dest'] = cnpj_dest
            infor['cnpj_cpf_dest_len'] = len(cnpj_dest)
        else:
            infor['cnpj_cpf_dest'] = cpf_dest
            infor['cnpj_cpf_dest_len'] = len(cpf_dest)
        
        
        infor['dest_name'] = dest_name
        return infor
    elif modelo_nfe.text == '55':
        infor = {
            'Serie': serie.text,
            'Numero_da_Nota': numero.text,
            'Emitente': emitente,
            'CNPJ_Emitente': cnpj_emit_format,
            'Chave_de_Acesso': chave_acesso,
            'op': op,
            'infcpl': infcpl,
            'produtos': produtos,
            'xml': xml_sem_namespace_format,
            'modelo': modelo_nfe.text,
            'alq_validado': alq_validado,
            'erro_pagamento': erro_pagamento,
            'data': data_formatada,
            'cnpj_cpf_dest': cnpj_dest,
            'dest_name': dest_name
        }
        if cnpj_dest is not None:
            infor['cnpj_cpf_dest'] = cnpj_dest
            infor['dest_name'] = dest_name
        else:
            infor['cnpj_cpf_dest'] = cpf_dest
            infor['dest_name'] = dest_name
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
    
        

def calc_fisco(root, caminho, nsNFE):
    produtos = []
    for det in root.findall(caminho + 'ns:det', nsNFE):
        caminho_icms = det.find('ns:imposto/ICMS/ns:ICMS00/ns:CST', nsNFE)
        if caminho_icms is not None:
            caminho_icms = 'ns:imposto/ICMS/ns:ICMS00/'
        else:
            caminho_icms = 'ns:imposto/ICMS/ns:ICMS20/'

        cst = det.find(caminho_icms + 'ns:CST', nsNFE)
        valor_bc = det.find(caminho_icms + 'ns:vBC', nsNFE)
        picms = det.find(caminho_icms + 'ns:pICMS', nsNFE)
        vicms = det.find(caminho_icms + 'ns:vICMS', nsNFE)
        vprod = det.find(caminho + 'ns:prod/ns:vProd', nsNFE)
        produto = {
            'cst': cst,
            'valor_base': valor_bc.text,
            'alq_icms': picms,
            'valor_icms': vicms.text,
            'valor_prod': vprod.text
        }
        produtos.append(produto)

    base_tot = 0
    alq_icms = 0
    for produto in produtos:
        base_tot = float(produto['valor_base']) + base_tot
        if float(produto['alq_icms'].text) == 0:
            valida_uf_emit = local_emit(root, caminho, nsNFE)
