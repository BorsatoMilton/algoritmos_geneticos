import math
from metodos_auxiliares import realizar_recorrido, crear_poblacion_inicial, evaluar_poblacion, seleccion_por_torneo, crossover_ciclico, mutar


def ingresar_provincia(lista_filas, df):
    print("\nProvincias")
    print("---------")
    for i in range(len(lista_filas)):
        print(f"{i + 1}. {lista_filas[i]}")

    provincia_partida_num = int(input("Ingrese el número de la provincia: "))
    while provincia_partida_num < 1 or provincia_partida_num > len(lista_filas):
        print("Número de provincia inválido. Intente nuevamente.")
        provincia_partida_num = int(input("Ingrese el número de la provincia: "))

    nombre_partida = lista_filas[provincia_partida_num - 1]
    
    provincias_visitadas = [nombre_partida]
    provincias_restantes = lista_filas.copy()
    provincias_restantes.remove(nombre_partida)

    distancia_total = 0

    while len(provincias_restantes) > 0:
        provincias_visitadas, provincias_restantes, distancia = realizar_recorrido(provincias_visitadas, provincias_restantes, df)
        distancia_total += distancia


    distancia_regreso = df.loc[provincias_visitadas[-1], nombre_partida] # esto no se si es asi
    distancia_total += distancia_regreso
    provincias_visitadas.append(nombre_partida)

    print("\nCiudad de partida:", nombre_partida)
    print("Recorrido: ", provincias_visitadas)
    print("Distancia total: ", distancia_total)


def sin_ingresar_provincia(lista_filas, df):
    mejor_distancia_total = math.inf
    mejor_recorrido = []
    mejor_origen = None

    for origen_candidato in lista_filas:
        provincias_visitadas = [origen_candidato]
        provincias_restantes = lista_filas.copy()
        provincias_restantes.remove(origen_candidato)
        distancia_total = 0

        while len(provincias_restantes) > 0:
            provincias_visitadas, provincias_restantes, distancia = realizar_recorrido(provincias_visitadas, provincias_restantes, df)
            distancia_total += distancia
        
        distancia_regreso = df.loc[provincias_visitadas[-1], origen_candidato]
        distancia_total += distancia_regreso
        provincias_visitadas.append(origen_candidato)

        if distancia_total < mejor_distancia_total:
            mejor_distancia_total = distancia_total
            mejor_recorrido = provincias_visitadas
            mejor_origen = origen_candidato

    print(f"\nEl punto de partida automático óptimo es: {mejor_origen}")
    print("Recorrido Automático: ", mejor_recorrido)
    print("Distancia total mínima encontrada: ", mejor_distancia_total)


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
