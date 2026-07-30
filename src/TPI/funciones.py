import random
import pvlib
import numpy as np


def calcular_energia_anual(angulos, datos, sol, dni_extra, airmass, perdidas_sistema, potencia_pico_kwp):
    # angulos[0] = inclinación, angulos[1] = azimut
    
    """
    Fijarse esto, xq con calculadoras de internet a veces da distitno, no se si faltan parametros o se calcula de otra manera.
    O ver si la libreria es buena o existe otra mas exacta.
    """    

    irradiancia = pvlib.irradiance.get_total_irradiance(
        surface_tilt=angulos[0],
        surface_azimuth=angulos[1],
        solar_zenith=sol['apparent_zenith'],
        solar_azimuth=sol['azimuth'],
        dni=datos['radiacion_directa_normal'], 
        ghi=datos['radiacion_global_horizontal'],
        dhi=datos['radiacion_difusa_horizontal'],
        dni_extra=dni_extra,
        airmass=airmass,
        model='perez'
        )
    
    h_poa_kwh_m2 = irradiancia['poa_global'].sum() / 1000  # Wh/m² -> kWh/m²
    energia_kwh = h_poa_kwh_m2 * potencia_pico_kwp * (1 - perdidas_sistema)
    return energia_kwh



def crossover_aritmetico(padre1, padre2, alpha=None):
    if alpha is None:
        alpha = np.random.rand()
    
    hijo1 = [0, 0]
    hijo2 = [0, 0]

    hijo1[0] = alpha * padre1[0] + (1 - alpha) * padre2[0]
    hijo1[1] = alpha * padre1[1] + (1 - alpha) * padre2[1]
    
    hijo2[0] = (1 - alpha) * padre1[0] + alpha * padre2[0]
    hijo2[1] = (1 - alpha) * padre1[1] + alpha * padre2[1]
    
    return hijo1, hijo2


def seleccion_torneo(poblacion, fitness, k=3):

    indices_candidatos = random.sample(range(len(poblacion)), k)
    
    mejor_indice = max(indices_candidatos, key=lambda i: fitness[i])
    
    return poblacion[mejor_indice]