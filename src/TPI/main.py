import random
import numpy as np
from pvlib.iotools import get_pvgis_tmy
from funciones import crossover_aritmetico, seleccion_torneo, calcular_energia_anual
import pvlib




def ejecutar_optimizacion(datos_clima, latitude, longitude, sol, dni_extra, airmass, pop_size=100, n_generaciones=30):
    # [inclinación, azimut]
    poblacion = np.random.rand(pop_size, 2) * [90, 360]


    
    for gen in range(n_generaciones):

        fitness = np.array([calcular_energia_anual(ind, datos_clima, sol, dni_extra, airmass, perdidas_sistema=0.14, potencia_pico_kwp=1.0) for ind in poblacion])
        

        indices_ordenados = np.argsort(fitness)[::-1]
        poblacion = poblacion[indices_ordenados]
        fitness = fitness[indices_ordenados]
        

        nueva_poblacion = [poblacion[0], poblacion[1]] 
        
        while len(nueva_poblacion) < pop_size:

            padre1 = seleccion_torneo(poblacion, fitness)
            padre2 = seleccion_torneo(poblacion, fitness)
            
            # Crossover

            if random.random() < 0.85:  
                hijo1, hijo2 = crossover_aritmetico(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()


            # Mutación
            if random.random() < 0.15: 
                hijo1 += np.random.normal(0, 5, size=2)
                hijo1[0] = np.clip(hijo1[0], 0, 90)  
                hijo1[1] = np.clip(hijo1[1], 0, 360)   

            if random.random() < 0.15:  
                hijo2 += np.random.normal(0, 5, size=2)
                hijo2[0] = np.clip(hijo2[0], 0, 90)
                hijo2[1] = np.clip(hijo2[1], 0, 360)

            print("Hijo 1:", hijo1, "Hijo 2:", hijo2)
            nueva_poblacion.append(hijo1)
            nueva_poblacion.append(hijo2)


        poblacion = np.array(nueva_poblacion)
        print(f"Generación {gen}: Mejor Energía = {fitness[0]:.2f}")

    return poblacion[0]


def main():
    latitude = -32.94
    longitude = -60.63

    data, meta = get_pvgis_tmy(latitude=latitude, longitude=longitude, usehorizon=True, coerce_year=2025) 
    # devuelve un dataFrame con temperatura aure, humedad, ghi, dni, dhi, IR(h), vel viento, direccion viento, presion.

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

    sol = pvlib.solarposition.get_solarposition(time=data.index, latitude=latitude, longitude=longitude) 
    dni_extra = pvlib.irradiance.get_extra_radiation(data.index)
    airmass = pvlib.atmosphere.get_relative_airmass(sol['apparent_zenith'])

    mejor_config = ejecutar_optimizacion(data, latitude, longitude, sol, dni_extra, airmass)

    angulos_tradicionales = [abs(latitude), 0.0]  # [32.94, 0.0] PREGUNTARLE A MARINO, no se si esta bien
    energia_tradicional = calcular_energia_anual(
        angulos_tradicionales, data, sol, dni_extra, airmass, 0.14, 1.0
    )
    energia_optimizada = calcular_energia_anual(
        mejor_config, data, sol, dni_extra, airmass, 0.14, 1.0
    )

    ganancia_porcentaje = ((energia_optimizada - energia_tradicional) / energia_tradicional) * 100
    print(f"\n--- COMPARACIÓN GA vs. TRADICIONAL ---")
    print(f"Energía método tradicional (32.94°, 0.0°): {energia_tradicional:.2f} kWh/año")
    print(f"Energía método optimizado  ({mejor_config[0]:.2f}°, {mejor_config[1]:.2f}°): {energia_optimizada:.2f} kWh/año")
    print(f"Mejora conseguida con GA: {ganancia_porcentaje:.2f}%")
    print(f"Inclinación: {mejor_config[0]:.2f}, Azimut: {mejor_config[1]:.2f}")


if __name__ == "__main__":
    main()