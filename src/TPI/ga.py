import random
import time
import numpy as np

from funciones import crossover_aritmetico, seleccion_torneo, calcular_energia_anual


def ejecutar_optimizacion(
    datos_clima, sol, dni_extra, airmass,
    pop_size=100, n_generaciones=30,
    prob_crossover=0.85, prob_mutacion=0.15, sigma_mutacion=5.0,
    perdidas_sistema=0.14, potencia_pico_kwp=1.0,
    seed=None, verbose=True
):
    """
    Ejecuta el GA y devuelve, además del mejor individuo, el historial
    de convergencia (mejor fitness por generación) y el tiempo total,
    necesarios para el Objetivo 5 (precisión / convergencia / mejora %).
    """
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    poblacion = np.random.rand(pop_size, 2) * [90, 360]
    historial_mejor = []
    t0 = time.time()

    mejor_fitness_global = -np.inf
    mejor_individuo_global = None

    for gen in range(n_generaciones):
        fitness = np.array([
            calcular_energia_anual(ind, datos_clima, sol, dni_extra, airmass,
                                    perdidas_sistema, potencia_pico_kwp)
            for ind in poblacion
        ])

        indices_ordenados = np.argsort(fitness)[::-1]
        poblacion = poblacion[indices_ordenados]
        fitness = fitness[indices_ordenados]

        if fitness[0] > mejor_fitness_global:
            mejor_fitness_global = fitness[0]
            mejor_individuo_global = poblacion[0].copy()

        historial_mejor.append(fitness[0])

        if verbose:
            print(f"Generación {gen}: Mejor Energía = {fitness[0]:.2f} kWh")

        # Elitismo: se preservan los 2 mejores
        nueva_poblacion = [poblacion[0].copy(), poblacion[1].copy()]

        while len(nueva_poblacion) < pop_size:
            padre1 = seleccion_torneo(poblacion, fitness)
            padre2 = seleccion_torneo(poblacion, fitness)

            if random.random() < prob_crossover:
                hijo1, hijo2 = crossover_aritmetico(padre1, padre2)
            else:
                hijo1, hijo2 = padre1.copy(), padre2.copy()

            if random.random() < prob_mutacion:
                hijo1 = hijo1 + np.random.normal(0, sigma_mutacion, size=2)
                hijo1[0] = np.clip(hijo1[0], 0, 90)
                hijo1[1] = np.clip(hijo1[1], 0, 360)

            if random.random() < prob_mutacion:
                hijo2 = hijo2 + np.random.normal(0, sigma_mutacion, size=2)
                hijo2[0] = np.clip(hijo2[0], 0, 90)
                hijo2[1] = np.clip(hijo2[1], 0, 360)

            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < pop_size:
                nueva_poblacion.append(hijo2)

        poblacion = np.array(nueva_poblacion)

    tiempo_total = time.time() - t0
    return mejor_individuo_global, historial_mejor, tiempo_total