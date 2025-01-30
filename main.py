import requests

from db import models
from lib.xml_helper import xml_to_dict

# Create the table if does not exists
models.Well.create_table()

def main():

    # URL del servicio OData v3
    url = "http://datos.energia.gob.ar/datastore/odata3.0/cb5c0f04-7835-45cd-b982-3e25ca7d7751"

    # Parámetros de la consulta OData (opcional)
    params = {
        "$select": "empresa",
        "$orderby": "provincia",
        "$top": 500,                 # Limitar el número de resultados
        "$skip": 1000,
        "$filter": "idpozo eq 214",  # Filtrar productos con precio mayor a 10
    }

    # Call GET request
    response = requests.get(url, params=params)
    # print("---------------------------------\n",response.text,"---------------------------------\n")

    # Verify if the request was successful
    if response.status_code == 200:
        
        # Transform the XML response to a Python dictionary
        data = xml_to_dict(response.content)


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
        
        print("\n--\n")
        print(record_count)
        print(response.request.url)
        print(response.status_code)
        print(response.request.headers)
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    main()