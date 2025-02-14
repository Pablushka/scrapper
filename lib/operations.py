from yaspin import yaspin
import requests
import json

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

spinner = yaspin()


@yaspin(text="Fetching structure and data...", color="green")
def fetch_data(url, params=empresas_params):
    """
    Fetch data from the given URL with specified parameters.

    Args:
        url (str): The URL to fetch data from.
        params (dict): The parameters to include in the request.

    Returns:
        tuple: A tuple containing fields and data.
    """
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

    return data


@yaspin(text="Fetching structure and data...", color="green")
def fetch_columns(url, params=empresas_params):
    """
    Fetch data from the given URL with specified parameters.

    Args:
        url (str): The URL to fetch data from.
        params (dict): The parameters to include in the request.

    Returns:
        tuple: A tuple containing fields and data.
    """
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


@yaspin(spinner=spinner, text="Fetching companies from remote server...", color="yellow")
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
    # spinner.color('green')
    spinner.ok("✔")  # Show a success marker
    if response.status_code == 200:
        all_companies = [empresa['empresa'] for empresa in response.json()
                         ['result']['records'] if empresa['empresa']]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        spinner.fail("✘")  # Show a failure marker
        exit()

    return all_companies
