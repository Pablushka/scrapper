import inquirer
import typer
import json
from rich.console import Console
from rich.table import Table

app = typer.Typer()


def print_json_table(title="Data", json_data=None):
    """Print JSON data as a user-friendly table using Rich."""
    console = Console()

    # Create a table
    table = Table(title=title, show_header=True,
                  header_style="bold magenta")

    # Add columns dynamically based on JSON keys
    if isinstance(json_data, list) and len(json_data) > 0:
        if isinstance(json_data[0], str):
            table.add_column("Column", style="dim")
            table.add_row(*json_data)
        else:
            for key in json_data[0].keys():
                table.add_column(key, style="dim")

            # Add rows
            for item in json_data:
                table.add_row(*[str(item.get(key, ""))
                                for key in item.keys()])
    else:
        typer.echo("No valid JSON data found or JSON is not a list.")

    # Print the table
    console.print(table)


def select_companies(empresas: list) -> list:
    """Prompt the user to select multiple companies."""
    questions = [
        inquirer.Checkbox(
            'companies',
            message="Select at least one company",
            choices=empresas
        ),
    ]
    answers = inquirer.prompt(questions)

    return answers['companies'] if answers else []


def select_fields(fields: list, default: list = ["idpozo", "empresa", "yacimiento", "area"]) -> list:
    """Prompt the user to select multiple fields."""

    choices = [(field, True if field in default else False)
               for field in fields]

    questions = [
        inquirer.Checkbox(
            'fields',
            message="Select at least one field",
            choices=fields,
            default=[field for field in fields if field in default]
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['fields']
