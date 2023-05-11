from lxml import etree
import pathlib
import xml.etree.ElementTree as ET

WORKING_DIR = str(pathlib.Path().resolve())
SCRIPT_DIR = str(pathlib.Path(__file__).parent.resolve())

xml = etree.parse(SCRIPT_DIR + '/nfe.xml')

xml2 = etree.parse(SCRIPT_DIR + '/nfe2.xml')

xml_root = xml.getroot()

xml_root2 = xml2.getroot()

# print(etree.tostring(xml))

# print(xml_root.tag)

xml_schema = etree.XMLSchema(file=SCRIPT_DIR + '/schemas/nfe_v4.00.xsd')

xml_schema2 = etree.XMLSchema(file=SCRIPT_DIR + '/schema.xsd')

# print('Tag raiz do XML: ' + xml_root.tag)

# print(xml_schema.validate(xml))

# if xml_schema.assertValid(xml_root) is None:
#     print('sucesso')

# if xml_schema2.assertValid(xml2) is None:
#     print('sucesso 2')

xml_schema.validate(xml)

log = xml_schema.error_log

error = log.last_error

print(error)
