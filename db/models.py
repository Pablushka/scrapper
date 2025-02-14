from peewee import *
from datetime import datetime
import json

db = SqliteDatabase('wells.db')


class Well(Model):
    # Identification
    id = AutoField(primary_key=True)
    idpozo = IntegerField(index=True)
    sigla = CharField(null=True)

    # Company and Location
    empresa = CharField(null=True, index=True)
    provincia = CharField(null=True, index=True)
    area = CharField(null=True)
    cod_area = CharField(null=True)
    yacimiento = CharField(null=True)
    cod_yacimiento = CharField(null=True)
    cuenca = CharField(null=True)

    # Technical Details
    tipo_recurso = CharField(null=True)
    sub_tipo_recurso = CharField(null=True)
    tipopozo = CharField(null=True)
    tipoextraccion = CharField(null=True)
    tipoestado = CharField(null=True)
    clasificacion = CharField(null=True)
    subclasificacion = CharField(null=True)
    formacion = CharField(null=True)
    gasplus = CharField(null=True)

    # Measurements
    cota = FloatField(null=True)
    profundidad = FloatField(null=True)

    # Dates
    adjiv_fecha_inicio_perf = DateTimeField(null=True)
    adjiv_fecha_fin_perf = DateTimeField(null=True)
    adjiv_fecha_inicio_term = DateTimeField(null=True)
    adjiv_fecha_fin_term = DateTimeField(null=True)

    # Geospatial
    geojson = TextField(null=True)
    geom = CharField(null=True)
    latitude = FloatField(null=True)
    longitude = FloatField(null=True)

    class Meta:
        database = db
        indexes = (
            (('provincia', 'area'), False),
            (('tipo_recurso', 'tipopozo'), False),
            (('empresa', 'yacimiento'), False),
        )

    @property
    def coordinates(self):
        """Extract coordinates from geojson field"""
        if self.geojson:
            data = json.loads(self.geojson)
            return data.get('coordinates', [])
        return None


class WellProduction(Model):
    # Identification
    id = AutoField(primary_key=True)
    idpozo = IntegerField(index=True)
    idempresa = CharField(null=True)
    empresa = CharField(null=True, index=True)

    # Create sigla as foreign key
    sigla = ForeignKeyField(Well, field='sigla', backref='well_production')

    # sigla = CharField(null=True)

    # Production Data
    anio = IntegerField()
    mes = IntegerField()
    prod_pet = FloatField(default=0)
    prod_gas = FloatField(default=0)
    prod_agua = FloatField(default=0)
    iny_agua = FloatField(default=0)
    iny_gas = FloatField(default=0)
    iny_co2 = FloatField(default=0)
    iny_otro = FloatField(default=0)
    tef = FloatField(default=0)
    vida_util = FloatField(null=True)

    # Well Status
    tipoextraccion = CharField(null=True)
    tipoestado = CharField(null=True)
    tipopozo = CharField(null=True)
    formprod = CharField(null=True)

    # Location
    idareapermisoconcesion = CharField(null=True)
    areapermisoconcesion = CharField(null=True)
    idareayacimiento = CharField(null=True)
    areayacimiento = CharField(null=True)
    cuenca = CharField(null=True)
    provincia = CharField(null=True)
    coordenadax = FloatField(null=True)
    coordenaday = FloatField(null=True)

    # Technical Details
    profundidad = FloatField(null=True)
    formacion = CharField(null=True)
    tipo_de_recurso = CharField(null=True)
    proyecto = CharField(null=True)
    clasificacion = CharField(null=True)
    subclasificacion = CharField(null=True)
    sub_tipo_recurso = CharField(null=True)

    # Metadata
    fecha_data = DateTimeField()
    fechaingreso = DateTimeField()
    rectificado = BooleanField(default=False)
    habilitado = BooleanField(default=True)
    idusuario = IntegerField()
    observaciones = TextField(null=True)

    class Meta:
        table_name = 'well_production'
        database = db
        indexes = (
            (('idpozo', 'fecha_data'), True),  # Unique constraint
            (('empresa', 'sigla'), False),
            (('anio', 'mes'), False),
        )

# Create tables


def create_tables():
    with db:
        db.create_tables([Well, WellProduction])
