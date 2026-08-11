import pvlib
from pvlib.iotools import get_pvgis_tmy

LATITUDE = -32.94
LONGITUDE = -60.63
PERDIDAS_SISTEMA = 0.14
POTENCIA_PICO_KWP = 1.0

ANGULOS_TRADICIONALES = [abs(LATITUDE), 0.0] # habria que hablar con marino para este metodo

def cargar_datos_clima(latitude=LATITUDE, longitude=LONGITUDE):

    data, meta = get_pvgis_tmy(latitude=latitude, longitude=longitude,
                                usehorizon=True, coerce_year=2025)

    data = data.rename(columns={
        "temp_air": "temperatura_aire",
        "relative_humidity": "humedad_relativa", # No se utiliza en calculos, esta renombrado asi se renombra todo
        "ghi": "radiacion_global_horizontal",
        "dni": "radiacion_directa_normal",
        "dhi": "radiacion_difusa_horizontal",
        "IR(h)": "radiacion_infrarroja", # No se utiliza en calculos, esta renombrado asi se renombra todo
        "wind_speed": "velocidad_viento",
        "wind_direction": "direccion_viento", # No se utiliza en calculos, esta renombrado asi se renombra todo
        "pressure": "presion",
    })

    sol = pvlib.solarposition.get_solarposition(
        time=data.index, latitude=latitude, longitude=longitude
    )
    dni_extra = pvlib.irradiance.get_extra_radiation(data.index)
    airmass = pvlib.atmosphere.get_relative_airmass(sol['apparent_zenith'])

    return data, sol, dni_extra, airmass
