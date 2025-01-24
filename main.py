import requests
import xml.etree.ElementTree as ET
from typing import Dict, Any
from db import models

models.Well.create_table()

def xml_to_dict(element: ET.Element) -> Dict[str, Any]:
    """Convert XML to dictionary recursively."""
    result = {}
    
    # Handle attributes
    if element.attrib:
        result.update(element.attrib)
    
    # Handle children
    for child in element:
        # Remove namespace prefix from tags
        tag = child.tag.split('}')[-1]
        
        child_data = xml_to_dict(child)
        
        if tag in result:
            if not isinstance(result[tag], list):
                result[tag] = [result[tag]]
            result[tag].append(child_data)
        else:
            result[tag] = child_data
    
    # Handle text content
    if element.text and element.text.strip():
        if result:
            result['value'] = element.text.strip()
        else:
            result = element.text.strip()
    
    return result


def main():

    # URL del servicio OData v3 (ejemplo)
    url = "http://datos.energia.gob.ar/datastore/odata3.0/cb5c0f04-7835-45cd-b982-3e25ca7d7751"

    # Parámetros de la consulta OData (opcional)
    params = {
        "$select": "empresa",
        "$orderby": "provincia",
        "$top": 2,                 # Limitar el número de resultados
        "$skip": 0,
        "$filter": "idpozo eq 214",  # Filtrar productos con precio mayor a 10
    }

    # Call GET request
    response = requests.get(url, params=params)
    print("---------------------------------\n",response.text,"---------------------------------\n")

    # Verify if the request was successful
    if response.status_code == 200:
        
        # Transform the XML response to a Python dictionary
        data = xml_to_dict( ET.fromstring(response.content))


        # Process the data
        record_count = 0

        for entry in data['entry']:
            # print("\n")
            record_count+=1
            pozo = entry['content']['properties']

            # create a new well object with all the data from pozo
            

            well = models.Well.create(
                area=pozo['area'].get('value'),
                id = pozo['_id'].get('value'),
                idpozo=pozo['idpozo'].get('value'),
                empresa=pozo['empresa'].get('value'),
                provincia=pozo['provincia']['value'],
                tipo_recurso=pozo['tipo_recurso']['value'],
                tipopozo=pozo['tipopozo']['value'],
                sub_tipo_recurso=pozo['sub_tipo_recurso']['value'],
                cota=pozo['cota'].get('value'),
                profundidad=pozo['profundidad'].get('value'),
                geojson=pozo['geojson'].get('value'),
                geom=pozo['geom'].get('value'),
                cuenca=pozo['cuenca'].get('value'),
                gasplus=pozo['gasplus'].get('value'),

                

            )
            print(well)
        
        print("--\n")
        print(record_count)
        print(response.request.url)
        print(response.status_code)
        print(response.request.headers)
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()