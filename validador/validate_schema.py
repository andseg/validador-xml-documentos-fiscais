from lxml import etree
import pathlib

WORKING_DIR = str(pathlib.Path().resolve())
SCRIPT_DIR = str(pathlib.Path(__file__).parent.resolve())

def validate_schema(file):
    schema_path = '/schemas/'
    xml = etree.parse(file)
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
    
    xml_schema = etree.XMLSchema(file=SCRIPT_DIR + schema_path)

    xml_schema.validate(xml)

    log = xml_schema.error_log

    error = log.last_error
    
    if not xml_schema(xml):
        response = xml_schema.error_log.last_error

    if error:
        print(error)
    else:
        print('Validado sem erros')