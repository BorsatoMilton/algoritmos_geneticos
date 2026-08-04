import random
import pvlib
import numpy as np


def calcular_energia_anual(angulos, datos, sol, dni_extra, airmass, perdidas_sistema, potencia_pico_kwp):
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

    params_temp = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']
    temp_celda = pvlib.temperature.sapm_cell(
        irradiancia['poa_global'],
        datos['temperatura_aire'],
        datos['velocidad_viento'],
        **params_temp
    )

    gamma_pdc = -0.004
    potencia_m2 = irradiancia['poa_global'] * (1 + gamma_pdc * (temp_celda - 25))

    energia_kwh = (potencia_m2.sum() / 1000) * potencia_pico_kwp * (1 - perdidas_sistema)
    return energia_kwh


def crossover_aritmetico(padre1, padre2, alpha=None):
    if alpha is None:
        alpha = np.random.rand()

    padre1 = np.asarray(padre1, dtype=float)
    padre2 = np.asarray(padre2, dtype=float)

    hijo1 = alpha * padre1 + (1 - alpha) * padre2
    hijo2 = (1 - alpha) * padre1 + alpha * padre2

    return hijo1, hijo2


def seleccion_torneo(poblacion, fitness, k=3):
    indices_candidatos = random.sample(range(len(poblacion)), k)
    mejor_indice = max(indices_candidatos, key=lambda i: fitness[i])
    return poblacion[mejor_indice]