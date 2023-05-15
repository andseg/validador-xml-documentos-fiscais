from lxml import etree
import pathlib

WORKING_DIR = str(pathlib.Path().resolve())
SCRIPT_DIR = str(pathlib.Path(__file__).parent.resolve())

schema_file = '/schemas/'

# NF-e usada para teste
# NUNCA ENVIAR ESSA NF-E PARA O GITHUB. DEIXE A NFE NO .gitignore
xml = etree.parse(SCRIPT_DIR + '/nfe.xml')

xml_root = xml.getroot()

if xml_root.tag.__contains__('consReciNFe'):
    schema_file += 'consReciNFe_v4.00.xsd'
elif xml_root.tag.__contains__('consSitNFe'):
    schema_file += 'consSitNFe_v4.00.xsd'
elif xml_root.tag.__contains__('consStatServ'):
    schema_file += 'consStatServ_v4.00.xsd'
elif xml_root.tag.__contains__('enviNFe'):
    schema_file += 'enviNFe_v4.00.xsd'
elif xml_root.tag.__contains__('inutNFe'):
    schema_file += 'inutNFe_v4.00.xsd'
elif xml_root.tag.__contains__('NFe'):
    schema_file += 'nfe_v4.00.xsd'
elif xml_root.tag.__contains__('ProcInutNFe'):
    schema_file += 'procInutNFe_v4.00.xsd'
elif xml_root.tag.__contains__('nfeProc'):
    schema_file += 'procNFe_v4.00.xsd'
elif xml_root.tag.__contains__('retConsReciNFe'):
    schema_file += 'retConsReciNFe_v4.00.xsd'
elif xml_root.tag.__contains__('retConsSitNFe'):
    schema_file += 'retConsSitNFe_v4.00.xsd'
elif xml_root.tag.__contains__('retConsStatServ'):
    schema_file += 'retConsStatServ_v4.00.xsd'
elif xml_root.tag.__contains__('retEnviNFe'):
    schema_file += 'retEnviNFe_v4.00.xsd'
elif xml_root.tag.__contains__('retInutNFe'):
    schema_file += 'retInutNFe_v4.00.xsd'
elif xml_root.tag.__contains__('Signature'):
    schema_file += 'xmldsig-core-schema_v1.01.xsd'

xml_schema = etree.XMLSchema(file=SCRIPT_DIR + schema_file)

xml_schema.validate(xml)

log = xml_schema.error_log

error = log.last_error

if error:
    print(error)
else:
    print('Validado sem erros')
