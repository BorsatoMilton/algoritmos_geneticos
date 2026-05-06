import matplotlib.pyplot as plt
import numpy as np
from funciones_auxiliares import calcular_funcion_objetivo


def generar_grafica(resultados_todas_corridas, metodo, corridas, ciclos):

    maximos = np.zeros(ciclos)
    minimos = np.zeros(ciclos)
    promedios = np.zeros(ciclos)

    for corrida in resultados_todas_corridas:
        for gen_idx, (mejor, peor, promedio, _) in enumerate(corrida):
            maximos[gen_idx] += calcular_funcion_objetivo(mejor[1])
            minimos[gen_idx] += calcular_funcion_objetivo(peor[1])
            promedios[gen_idx] += promedio

    maximos /= corridas
    minimos /= corridas
    promedios /= corridas

    generaciones = np.arange(1, ciclos + 1)

    plt.figure(figsize=(10, 6))
    plt.plot(generaciones, maximos, label='Máximo', color='green', marker='o', markersize=4, linewidth=2)
    plt.plot(generaciones, promedios, label='Promedio', color='blue', marker='s', markersize=4, linewidth=2)
    plt.plot(generaciones, minimos, label='Mínimo', color='red', marker='^', markersize=4, linewidth=2)

    plt.xlabel('Generación')
    plt.ylabel('Función Objetivo  f(x) = (x / (2³⁰ - 1))²')
    plt.title(f'Valores de la Función Objetivo por Generación\nMétodo: {metodo.upper()} | {corridas} Corridas | {ciclos} Generaciones')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(generaciones)
    plt.tight_layout()
    plt.show()


