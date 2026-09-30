import math
from metodos_auxiliares import realizar_recorrido, crear_poblacion_inicial, evaluar_poblacion, seleccion_por_torneo, crossover_ciclico, mutar


def iniciar_recorrido(lista_filas, df, elegir_provincia):
    if elegir_provincia:
        print("\nProvincias")
        print("---------")
        for i in range(len(lista_filas)):
            print(f"{i + 1}. {lista_filas[i]}")

        provincia_partida_num = int(input("Ingrese el número de la provincia: "))
        while provincia_partida_num < 1 or provincia_partida_num > len(lista_filas):
            print("Número de provincia inválido. Intente nuevamente.")
            provincia_partida_num = int(input("Ingrese el número de la provincia: "))

        origenes_a_evaluar = [lista_filas[provincia_partida_num - 1]]
    else:
        origenes_a_evaluar = lista_filas

    mejor_distancia_total = math.inf
    mejor_recorrido = []
    mejor_origen = None
    recorridos = []

    for origen in origenes_a_evaluar:
        provincias_visitadas = [origen]
        provincias_restantes = lista_filas.copy()
        provincias_restantes.remove(origen)
        distancia_total = 0

        while len(provincias_restantes) > 0:
            provincias_visitadas, provincias_restantes, distancia = realizar_recorrido(provincias_visitadas, provincias_restantes, df)
            distancia_total += distancia

        distancia_regreso = df.loc[provincias_visitadas[-1], origen] 
        distancia_total += distancia_regreso
        provincias_visitadas.append(origen)
        recorridos.append((provincias_visitadas, distancia_total))

        if distancia_total < mejor_distancia_total:
            mejor_distancia_total = distancia_total
            mejor_recorrido = list(provincias_visitadas)
            mejor_origen = origen

    if elegir_provincia:
        print(f"\nCiudad de partida: {mejor_origen}")
        print(f"Recorrido: {mejor_recorrido}")
        print(f"Distancia total: {mejor_distancia_total}")
    else:
        print("\nRecorridos evaluados:")
        for i, (recorrido, distancia) in enumerate(recorridos):
            print(f"{i + 1} - Distancia total: {distancia} - Recorrido: {recorrido}")
        print(f"\nEl punto de partida óptimo es: {mejor_origen}")
        print(f"Recorrido: {mejor_recorrido}")
        print(f"Distancia total mínima encontrada: {mejor_distancia_total}")


def resolver_por_ag(lista_filas, df, n_poblacion=50, m_ciclos=200, prob_mutacion=0.1):
    tam_cromosoma = len(lista_filas)

    poblacion = crear_poblacion_inicial(tam_cromosoma, n_poblacion)
 
    mejor_recorrido_indices = None
    mejor_distancia = math.inf
 
    for ciclo in range(m_ciclos):
        fitness = evaluar_poblacion(poblacion, df, lista_filas)
 
        indice_mejor_actual = fitness.index(min(fitness))
        if fitness[indice_mejor_actual] < mejor_distancia:
            mejor_distancia = fitness[indice_mejor_actual]
            mejor_recorrido_indices = poblacion[indice_mejor_actual].copy()
 
        nueva_poblacion = []
        while len(nueva_poblacion) < n_poblacion:
            padre1 = seleccion_por_torneo(poblacion, fitness)
            padre2 = seleccion_por_torneo(poblacion, fitness)
 
            hijo1, hijo2 = crossover_ciclico(padre1, padre2)
 
            hijo1 = mutar(hijo1, prob_mutacion)
            hijo2 = mutar(hijo2, prob_mutacion)
 
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < n_poblacion:
                nueva_poblacion.append(hijo2)
 
        poblacion = nueva_poblacion
 
    mejor_recorrido_nombres = [lista_filas[i] for i in mejor_recorrido_indices]
    recorrido_completo = mejor_recorrido_nombres + [mejor_recorrido_nombres[0]]
    
    recorrido_numeros = [i + 1 for i in mejor_recorrido_indices] + [mejor_recorrido_indices[0] + 1]
    
    print(f"\nRecorrido Genético (en números): {recorrido_numeros}")
    print(f"Recorrido Genético (en provincias): {recorrido_completo}")
    print(f"Distancia total: {mejor_distancia:.2f}")
 
    return mejor_recorrido_nombres, mejor_distancia
