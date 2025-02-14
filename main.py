import typer
import json
from db import models
from lib.xml_helper import xml_to_dict
from typing import Optional
from rich import print
from lib.cli_ui import select_companies, print_json_table, select_fields
from yaspin import yaspin
from lib.operations import fetch_companies, fetch_data, update_wells, update_operations
from lib.models_fields import well_field_list, production_field_list


app = typer.Typer()


# Create the table if does not exists
# models.Well.create_table()
models.create_tables()


@app.command()
def main(limit: int = 500, offset: int = 0):
    # URL of the OData v3 service
    wells_url = "http://datos.energia.gob.ar/api/3/action/datastore_search"

    # Fetch all companies
    all_companies = fetch_companies(wells_url)
    # Select companies to process
    companies = select_companies(all_companies)
    # columns = select_fields(well_field_list)

    # Parameters for the wells data query
    wells_params = {
        "resource_id": "cb5c0f04-7835-45cd-b982-3e25ca7d7751",
        "fields": well_field_list,
        "q": "",
        "filters": json.dumps({"empresa": companies}),
        "limit": limit,
        "offset": offset
    }
    # Parameters for the production data query
    production_params = {
        "resource_id": "b5b58cdc-9e07-41f9-b392-fb9ec68b0725",
        "fields": production_field_list,
        "q": "",
        "filters": json.dumps({"empresa": companies}),
        "limit": limit,
        "offset": offset
    }

    # Fetch data with a spinner
    with yaspin(text="Fetching remote data...", color="green") as spinner:
        wells = fetch_data(wells_url, wells_params)
        production = fetch_data(wells_url, production_params)
        spinner.ok("✔")

        # Update wells data
        wells_count, wells_created, wells_rejected = update_wells(
            wells, spinner)
        spinner.write("✔ Wells data fetched successfully.")

        # Update production data
        production_records_count, production_records_created, production_records_rejected = update_operations(
            production)
        spinner.write("✔ Production data fetched successfully.")

    # Print summary of wells data processing
    print(f"\nTotal wells processed: {wells_count}")
    print(f"Total new wells stored: {wells_created}")
    print(f"Total wells rejected: {wells_rejected}")
    print(f"Total wells stored in database: {models.Well.select().count()}")

    # Print summary of production data processing
    print(f"\nTotal production records processed: {production_records_count}")
    print(f"Total new production records stored: {production_records_created}")
    print(f"Total production records rejected: {production_records_rejected}")
    print(
        f"Total production records stored in database: {models.WellProduction.select().count()}")


if __name__ == "__main__":
    app()
