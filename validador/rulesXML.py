import pandas as pd


def validator_rules(origin, dest, alq_nfe):
    alq_icms = pd.read_excel("./validador/aliquotas/aliquotaICMS.xlsx", index_col=0)
    alq = alq_icms.loc[origin, dest]
    for aliquota in alq_nfe:
        if float(aliquota.replace(" ' ", "")) != 0:
            if float(aliquota.replace(" ' ", "")) == alq:
                alq_validado = 'Alíquota ICMS Correta ' + origin + '-' + dest + ' Alíquota: ' + str(alq) + '%'
                return alq_validado
            else:
                alq_validado = 'Alíquota ICMS Incorreta ' + origin + '-' + dest + ' O correto seria: ' + str(alq) + '%'
                return alq_validado
        else:
            alq_validado = 'Inconsistência Encontrada não existe pICMS no arquivo'
            return alq_validado


def validador_rules_nfce(origin, alq_nfc):
    alq_icms = pd.read_excel("./validador/aliquotas/aliquotaICMS.xlsx", index_col=0)
    alq = alq_icms.loc[origin, origin]
    for aliquota in alq_nfc:
        if float(aliquota.replace(" ' ", "")) != 0:
            if float(aliquota.replace(" ' ", "")) == alq:
                alq_validado = 'Alíquota ICMS Correta ' + origin + ' Alíquota: ' + str(alq) + '%'
                return alq_validado
            else:
                alq_validado = 'Alíquota ICMS Incorreta ' + origin + ' O correto seria: ' + str(alq) + '%'
                return alq_validado
        else:
            alq_validado = 'Inconsistência Encontrada não existe pICMS no arquivo'
            return alq_validado


def rules_recebimentos(vpag, vnf):
    valor_total = sum(vpag)
    print(valor_total)
    if valor_total != vnf:
        diferenca = valor_total - vnf
        print('Valor Total da Nota (vNF) = R${}\n'
              'Valor Pago = R${}\n'
              'Diferença = R${}'.format(vnf, valor_total, diferenca))
    else:
        print('Valor Total da Nota (vNF) = R${}\n'
              'Valor Pago = R${}\n'.format(vnf, valor_total))
