import requests
from datetime import datetime
from odata import ODataService

# First, create the session
session = requests.Session()
url = 'http://datos.energia.gob.ar/api/3/action/package_show?id=produccion-de-petroleo-y-gas-por-pozo'
url = "http://datos.energia.gob.ar/dataset/c846e79c-026c-4040-897f-1ad3543b407c/resource/cb5c0f04-7835-45cd-b982-3e25ca7d7751/download/capitulo-iv-pozos.csv"

# Initialize service without base class first to generate the package
service = ODataService(
    url=url,
    session=session,
    reflect_entities=True,
    reflect_output_package="generated.produccion")