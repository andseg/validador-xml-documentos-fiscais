# Arquivo apenas para teste da codificação do lxml
from io import StringIO
from lxml import etree


# f = StringIO('''\
#  <xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
#  <xsd:element name="a" type="AType"/>
#  <xsd:complexType name="AType">
#    <xsd:sequence>
#      <xsd:element name="b" type="xsd:string" />
#    </xsd:sequence>
#  </xsd:complexType>
#  </xsd:schema>
#  ''')
# xmlschema_doc = etree.parse(f)
# xmlschema = etree.XMLSchema(xmlschema_doc)

# valid = StringIO('<a><b></b></a>')
# doc = etree.parse(valid)
# print(xmlschema.validate(doc))

# invalid = StringIO('<a><c></c></a>')
# doc2 = etree.parse(invalid)
# print(xmlschema.validate(doc2))

# invalid = StringIO('<a><c></c></a>')
# doc2 = etree.parse(invalid)
# if not xmlschema(doc2):
#     print("invalid!")
    
# err = ''    
# try:
#     xmlschema.assertValid(doc2)
# except Exception as e:
#     print(type(e).__name__ + " - " + str(e))
#     err = str(e)
    

# try:
#     xmlschema.assert_(doc2)
# except Exception as e:
#     print(type(e).__name__ + " - " + str(e))
#     err = str(e)
    
# log = xmlschema.error_log
# error = log.last_error
# error_domain = error.domain_name
# print(error.domain_name)
# error_type = error.type_name
# print(error.type_name)

# print('ERROR:'+error_domain+':'+error_type+':'+err)
        
file_teste = open('C:/Users/Dev/Andre/validador-xml-documentos-fiscais/nfe.xml', 'r')
xml_teste = etree.parse(file_teste)
file_teste.close()
xml_teste_root = xml_teste.getroot()
infor = {}
tags = ['mod','serie', 'nNF', 'emit', 'dest']
for element in xml_teste_root.iter(tag=etree.Element):
    tag = etree.QName(element).localname
    if tag in tags:
        infor[tag] = element.text
        for child in element.iterchildren():
             child_tag = etree.QName(child).localname
             child_text = child.text
             infor[child_tag] = child_text
        
print(infor)

    

    