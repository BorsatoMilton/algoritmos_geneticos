import pandas as pd
from pvlib.iotools import get_pvgis_tmy
import pvlib
import numpy as np

tiempos = pd.date_range(start='2026-01-01', end='2027-01-01', freq='h', tz='America/Argentina/Buenos_Aires')

data, meta = get_pvgis_tmy(latitude=-32.94, longitude=-60.63, usehorizon=True, coerce_year=2025) 
# devuelve un dataFrame con temperatura aure, humedad, ghi, dni, dhi, IR(h), vel viento, direccion viento, presion.

mejor_configuracion = [0,0]

data = data.rename(columns={
    "temp_air": "temperatura_aire",
    "relative_humidity": "humedad_relativa",
    "ghi": "radiacion_global_horizontal",     # GHI
    "dni": "radiacion_directa_normal",        # DNI
    "dhi": "radiacion_difusa_horizontal",     # DHI
    "IR(h)": "radiacion_infrarroja",
    "wind_speed": "velocidad_viento",
    "wind_direction": "direccion_viento",
    "pressure": "presion",
})

def calcular_energia_anual(angulos, datos):
    # angulos[0] = inclinación, angulos[1] = azimut
    
    sol = pvlib.solarposition.get_solarposition(time=datos.index, latitude=-32.94, longitude=-60.63)
    
    irradiancia = pvlib.irradiance.get_total_irradiance(
        surface_tilt=angulos[0],
        surface_azimuth=angulos[1],
        solar_zenith=sol['apparent_zenith'],
        solar_azimuth=sol['azimuth'],
        dni=datos['radiacion_directa_normal'], 
        ghi=datos['radiacion_global_horizontal'],
        dhi=datos['radiacion_difusa_horizontal']
    )
    
    # 3. La "Función Objetivo": Sumamos la irradiancia global incidente
    # Este es el valor que el Algoritmo Genético necesita maximizar
    return irradiancia['poa_global'].sum()



def ejecutar_optimizacion(datos_clima, pop_size=20, n_generaciones=30):
    # [inclinación, azimut]
    poblacion = np.random.rand(pop_size, 2) * [90, 360]
    
    for gen in range(n_generaciones):
        # 2. EVALUACIÓN (Fitness)
        fitness = np.array([calcular_energia_anual(ind, datos_clima) for ind in poblacion])
        
        # 3. SELECCIÓN (Elitismo)
        indices_ordenados = np.argsort(fitness)[::-1]
        poblacion = poblacion[indices_ordenados]
        fitness = fitness[indices_ordenados]
        
        # 4. REPRODUCCIÓN Y MUTACIÓN
        nueva_poblacion = [poblacion[0]] # El mejor siempre sobrevive (Elitismo), ver si cambiarlo
        
        while len(nueva_poblacion) < pop_size:
            """
            rehacer este while 
            """
            padre1 = poblacion[np.random.randint(0, pop_size // 2)]
            padre2 = poblacion[np.random.randint(0, pop_size // 2)]
            
            # Cruce: Promedio aritmético (o punto medio)
            hijo = (padre1 + padre2) / 2
            
            # Mutación: Introducimos variación aleatoria (0.1 de probabilidad)
            if np.random.rand() < 0.1:
                hijo += np.random.normal(0, 5, 2) 
            
            # Aseguramos que los ángulos sigan dentro de los límites físicos
            hijo = np.clip(hijo, [0, 0], [90, 360])
            nueva_poblacion.append(hijo)
            
        poblacion = np.array(nueva_poblacion)
        print(f"Generación {gen}: Mejor Energía = {fitness[0]:.2f}")

    return poblacion[0]

mejor_config = ejecutar_optimizacion(data)


print(mejor_config)