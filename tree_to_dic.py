import json
from lxml import etree
def elem2dict(node, attributes=True):
    """
    Convert an lxml.etree node tree into a dict.
    """
    result = {}
    if attributes:
        for item in node.attrib.items():
            key, result[key] = item

    for element in node.iterchildren():
        # Remove namespace prefix
        key = etree.QName(element).localname

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = elem2dict(element)
        if key in result:
            if type(result[key]) is list:
                result[key].append(value)
            else:
                result[key] = [result[key], value]
        else:
            result[key] = value
    return result




# TESTE DA FUNÇÃO
file_teste = open('C:/Users/Dev/Andre/validador-xml-documentos-fiscais/nfe.xml', 'r')
xml_teste = etree.parse(file_teste)
file_teste.close()
xml_teste_root = xml_teste.getroot()


dic = elem2dict(xml_teste_root)
print(json.dumps(dic, indent=4))

print(type(dic))

with open('tree_to_dic.json', 'w') as f:
    f.write(json.dumps(dic, indent=4))



