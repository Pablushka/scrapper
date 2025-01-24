import xml.etree.ElementTree as ET

def get_empresa_values(xml_file: str) -> list:
    # Define namespaces
    namespaces = {
        'd': 'http://schemas.microsoft.com/ado/2007/08/dataservices',
        'm': 'http://schemas.microsoft.com/ado/2007/08/dataservices/metadata'
    }
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find all entries and extract empresa values
    empresas = []
    for entry in root.findall('.//m:properties', namespaces):
        empresa = entry.find('d:empresa', namespaces)
        if empresa is not None:
            empresas.append(empresa.text)
    
    return empresas

# Usage example
xml_file = 'example.xml'
empresas = get_empresa_values(xml_file)
for empresa in empresas:
    print(f"Empresa: {empresa}")