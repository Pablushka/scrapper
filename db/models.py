from peewee import *
from datetime import datetime
import json

db = SqliteDatabase('wells.db')

class Well(Model):
    # Identification
    id = CharField(primary_key=True)
    idpozo = IntegerField(index=True)
    sigla = CharField(null=True)
    
    # Basic Info
    empresa = CharField(null=True)
    provincia = CharField(index=True)
    area = CharField(null=True)
    yacimiento = CharField(null=True)
    cod_area = CharField(null=True)
    cod_yacimiento = CharField(null=True)
    
    # Technical Details
    tipo_recurso = CharField(null=True)
    sub_tipo_recurso = CharField(null=True)
    tipopozo = CharField(index=True)
    tipoestado = CharField(null=True)
    tipoextraccion = CharField(null=True)
    clasificacion = CharField(null=True)
    subclasificacion = CharField(null=True)
    formacion = CharField(null=True)
    
    # Dates
    adjiv_fecha_inicio_perf = DateTimeField(null=True)
    adjiv_fecha_fin_perf = DateTimeField(null=True)
    adjiv_fecha_inicio_term = DateTimeField(null=True)
    adjiv_fecha_fin_term = DateTimeField(null=True)
    
    # Technical Measurements
    cota = FloatField(null=True)
    profundidad = FloatField(null=True)
    
    # Location
    geojson = TextField(null=True)  # Stored as JSON string
    geom = CharField(null=True)
    cuenca = CharField(null=True)
    
    # Additional Info
    gasplus = CharField(null=True)

    class Meta:
        database = db
        indexes = (
            (('provincia', 'area'), False),
            (('tipo_recurso', 'tipopozo'), False),
        )
    
    @property
    def coordinates(self):
        """Extract coordinates from geojson field"""
        if self.geojson:
            data = json.loads(self.geojson)
            return data.get('coordinates', [])
        return None

# Create tables
def create_tables():
    with db:
        db.create_tables([Well])