# IFM Wells Production Scrapper

This project is designed to scrape data from an OData v3 service, parse the XML response, and store the data into a SQLite database using the Peewee ORM.

## Project Structure

- `main.py`: The main script that performs the data scraping and storage.
- `db/models.py`: Defines the database models and handles database interactions.
- `test1.py`: Contains utility functions for loading and parsing XML data.
- `example.xml`: An example XML file used for testing.

## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository_url>
    cd IFM/vista/scrapper
    ```

2. **Create a virtuan environmet
    ```sh
    python -m venv .venv
    ```

3. **Activate de virtual environment**
    If you use Windows
    ```sh
    .\venv\Scripts\activate.ps1
    ```

4. **Install dependencies:**
    ```sh
    pip install requests peewee
    ```

5. **Create the database:**
    ```sh
    python -c "from db.models import create_tables; create_tables()"
    ```

## Usage

1. **Run the main script:**
    ```sh
    python main.py
    ```

    This will fetch data from the OData service, parse the XML response, and store the data into the SQLite database.

2. **Test with example XML:**
    ```sh
    python test1.py
    ```

    This will load and parse the `example.xml` file and print the well data.

## Project Details

### main.py

- Fetches data from the OData service.
- Parses the XML response using `xml_to_dict`.
- Stores the data into the SQLite database using Peewee ORM.

### db/models.py

- Defines the `Well` model representing the well data.
- Handles database creation and interactions.

### test1.py

- Contains utility functions to load XML content and parse it into `Well` model instances.

### example.xml

- An example XML file used for testing the parsing functionality.

## License

This project is licensed under the MIT License.