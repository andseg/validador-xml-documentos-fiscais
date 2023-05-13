import pandas as pd
import xml.etree.ElementTree as ET
import xml.dom.minidom


def walks_xml(file, caminho):
    root = file.getroot()
    print(root, caminho)
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
        print(xml_formatado)


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
                    alq_validado = 'Alíquota ICMS utilizado:' + aliquota + '%' + '  Origem: ' + origin + '  Destino: ' + dest + ' O correto seria: ' + str(alq) + '%'
                    return alq_validado
            else:

                alq_validado = 'Inconsistência Encontrada não existe pICMS no arquivo'
                return alq_validado

    else:
        alq_icms = pd.read_excel("./validador/aliquotas/aliquotaICMS.xlsx", index_col=0)
        alq = alq_icms.loc[origin, origin]
        for aliquota in alq_nfe:
            print(aliquota)
            if float(aliquota.replace(" ' ", "")) != 0:
                if float(aliquota.replace(" ' ", "")) == alq:
                    alq_validado = 'Alíquota ICMS Correta ' + origin + ' Alíquota: ' + str(alq) + '%'
                    return alq_validado
                else:
                    alq_validado = 'Alíquota ICMS utilizado:' + aliquota + '%' + '  Origem: ' + origin + '  Destino: ' + dest + ' o correto seria: ' + str(alq) + '%'
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
        retorno = ('vPag Erro   ' + 'Valor Total = R$' + str(vnf) + '   Valor Pago = R$' + str(valor_total) + '    Diferença = R$' + str(diferenca))
        return retorno
    else:
        retorno = 'vPag - OK'
        return retorno
