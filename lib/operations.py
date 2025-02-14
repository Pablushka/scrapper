import requests
import json
from db import models
from rich import print
from rich.table import Table

headers = {
    "Content-Type": "application/json"
}

empresas_params = {
    "resource_id": "cb5c0f04-7835-45cd-b982-3e25ca7d7751",
    "plain": "false&resource_id=cb5c0f04-7835-45cd-b982-3e25ca7d7751",
    "limit": 200,
    "offset": 0,
    "include_total": "false",
    "fields": "empresa",
    "distinct": "true",
    "sort": "empresa"
}


def fetch_data(url, params=empresas_params):

    response = requests.post(url, headers=headers,
                             params=params)

    if response.status_code != 200:
        # print(f"Error: {response.status_code} - {response.text}")
        print('\n')
        print(response.text)
        return []

    json_response = response.json()

    data = json_response['result']['records']

    for record in data:
        if 'geojson' in record:
            # Parse geojson string to dict
            geojson_data = json.loads(record['geojson'])
            # Extract coordinates
            coordinates = geojson_data.get('coordinates', [0, 0])
            # Add new properties
            record['longitude'] = coordinates[0]
            record['latitude'] = coordinates[1]
            # Optionally remove original geojson
            del record['geojson']

    return data


def fetch_columns(url, params=empresas_params):

    response = requests.post(url, headers=headers,
                             params=params)

    json_response = response.json()

    data = json_response['result']['records']

    for record in data:
        if 'geojson' in record:
            # Parse geojson string to dict
            geojson_data = json.loads(record['geojson'])
            # Extract coordinates
            coordinates = geojson_data.get('coordinates', [0, 0])
            # Add new properties
            record['longitude'] = coordinates[0]
            record['latitude'] = coordinates[1]
            # Optionally remove original geojson
            del record['geojson']

    fields = list(data[0].keys()) if data else []
    fields.sort()  # Sort fields in ascending order

    return fields


def fetch_companies(url, empresas_params=empresas_params):
    """
    Fetch companies from the given URL with specified parameters.

    Args:
        url (str): The URL to fetch companies from.
        empresas_params (dict): The parameters to include in the request.

    Returns:
        list: A list of company names.
    """
    response = requests.get(url, empresas_params, headers=headers)

    if response.status_code == 200:
        all_companies = [empresa['empresa'] for empresa in response.json()
                         ['result']['records'] if empresa['empresa']]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        exit()

    return all_companies


def update_wells(wells: list, spinner):
    # Process the data
    record_count = 0

    # Rejected wells
    rejected_wells = Table(title="Pozos rechazados",
                           show_header=True, expand=True, safe_box=True)
    rejected_wells.add_column("Sigla", style="dim", width=12)
    rejected_wells.add_column("Motivo", style="dim")

    new_wells = 0

    # with yaspin(text="Creating wells data...", color="green") as spinner:
    for well_data in wells:
        record_count += 1

        # spinner.text = f"Processing well {record_count}..."

        # Parse geojson for coordinates
        coordinates = [0, 0]
        if 'geojson' in well_data:
            geojson_data = json.loads(well_data['geojson'])
            coordinates = geojson_data.get('coordinates', [0, 0])

        # Extract nested values
        provincia = well_data.get('provincia')
        tipo_recurso = well_data.get('tipo_recurso')
        tipopozo = well_data.get('tipopozo')
        sub_tipo_recurso = well_data.get('sub_tipo_recurso')

        is_new = not models.Well.select().where(
            models.Well.sigla == well_data.get('sigla')).exists()

        if is_new:
            # Create well record with all fields
            well = models.Well.create(
                idpozo=well_data.get('idpozo'),
                sigla=well_data.get('sigla'),
                empresa=well_data.get('empresa'),
                provincia=provincia,
                area=well_data.get('area'),
                cod_area=well_data.get('cod_area'),
                yacimiento=well_data.get('yacimiento'),
                cod_yacimiento=well_data.get('cod_yacimiento'),
                cuenca=well_data.get('cuenca'),
                tipo_recurso=tipo_recurso,
                sub_tipo_recurso=sub_tipo_recurso,
                tipopozo=tipopozo,
                tipoextraccion=well_data.get('tipoextraccion'),
                tipoestado=well_data.get('tipoestado'),
                clasificacion=well_data.get('clasificacion'),
                subclasificacion=well_data.get('subclasificacion'),
                formacion=well_data.get('formacion'),
                gasplus=well_data.get('gasplus'),
                cota=float(well_data.get('cota', 0)),
                profundidad=float(well_data.get('profundidad', 0)),
                adjiv_fecha_inicio_perf=well_data.get(
                    'adjiv_fecha_inicio_perf'),
                adjiv_fecha_fin_perf=well_data.get('adjiv_fecha_fin_perf'),
                adjiv_fecha_inicio_term=well_data.get(
                    'adjiv_fecha_inicio_term'),
                adjiv_fecha_fin_term=well_data.get('adjiv_fecha_fin_term'),
                geojson=well_data.get('geojson'),
                geom=well_data.get('geom'),
                latitude=coordinates[1],
                longitude=coordinates[0]
            )
            new_wells += 1
        else:
            rejected_wells.add_row(
                well_data.get('sigla'), "Este pozo ya existe.")

    return record_count, new_wells, len(rejected_wells.rows)


def update_operations(operations: list):
    record_count = 0
    new_operations = 0

    # Rejected operations table
    rejected_operations = Table(title="Operaciones rechazadas",
                                show_header=True, expand=True, safe_box=True)
    rejected_operations.add_column("Sigla", style="dim", width=12)
    rejected_operations.add_column("Motivo", style="dim")

    # with yaspin(text="Creating operations data...", color="green") as spinner:
    for operation_data in operations:
        record_count += 1
        # spinner.text = f"Processing record {record_count}..."

        # Check if operation exists
        is_new = not models.WellProduction.select().where(
            (models.WellProduction.idpozo == operation_data.get('idpozo')) &
            (models.WellProduction.fecha_data ==
                operation_data.get('fecha_data'))
        ).exists()

        if is_new:
            # Create production record with all fields
            operation = models.WellProduction.create(
                # Identification
                idpozo=operation_data.get('idpozo'),
                idempresa=operation_data.get('idempresa'),
                empresa=operation_data.get('empresa'),
                sigla=operation_data.get('sigla'),

                # Production Data
                anio=operation_data.get('anio'),
                mes=operation_data.get('mes'),
                prod_pet=float(operation_data.get('prod_pet', 0)),
                prod_gas=float(operation_data.get('prod_gas', 0)),
                prod_agua=float(operation_data.get('prod_agua', 0)),
                iny_agua=float(operation_data.get('iny_agua', 0)),
                iny_gas=float(operation_data.get('iny_gas', 0)),
                iny_co2=float(operation_data.get('iny_co2', 0)),
                iny_otro=float(operation_data.get('iny_otro', 0)),
                tef=float(operation_data.get('tef', 0)),
                vida_util=float(operation_data.get('vida_util')) if operation_data.get(
                    'vida_util') else None,

                # Well Status
                tipoextraccion=operation_data.get('tipoextraccion'),
                tipoestado=operation_data.get('tipoestado'),
                tipopozo=operation_data.get('tipopozo'),
                formprod=operation_data.get('formprod'),

                # Location
                idareapermisoconcesion=operation_data.get(
                    'idareapermisoconcesion'),
                areapermisoconcesion=operation_data.get(
                    'areapermisoconcesion'),
                idareayacimiento=operation_data.get('idareayacimiento'),
                areayacimiento=operation_data.get('areayacimiento'),
                cuenca=operation_data.get('cuenca'),
                provincia=operation_data.get('provincia'),
                coordenadax=float(operation_data.get('coordenadax', 0)),
                coordenaday=float(operation_data.get('coordenaday', 0)),

                # Technical Details
                profundidad=float(operation_data.get('profundidad', 0)),
                formacion=operation_data.get('formacion'),
                tipo_de_recurso=operation_data.get('tipo_de_recurso'),
                proyecto=operation_data.get('proyecto'),
                clasificacion=operation_data.get('clasificacion'),
                subclasificacion=operation_data.get('subclasificacion'),
                sub_tipo_recurso=operation_data.get('sub_tipo_recurso'),

                # Metadata
                fecha_data=operation_data.get('fecha_data'),
                fechaingreso=operation_data.get('fechaingreso'),
                rectificado=operation_data.get('rectificado') == 't',
                habilitado=operation_data.get('habilitado') == 't',
                idusuario=int(operation_data.get('idusuario', 0)),
                observaciones=operation_data.get('observaciones')
            )
            new_operations += 1
        else:
            rejected_operations.add_row(
                operation_data.get('sigla'),
                f"Ya existe producción para el pozo {operation_data.get('sigla')} en la fecha {operation_data.get('fecha_data')}"
            )

    return record_count, new_operations, len(rejected_operations.rows)
