def handle_uploaded_file(f):
    xml_as_string = ''
    for chunk in f.chunks():
        xml_as_string += chunk.decode('utf-8')
    return xml_as_string
            