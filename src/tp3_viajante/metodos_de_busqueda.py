import math
import pandas as pd
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


def resolver_por_ag(lista_filas, df, n_poblacion=50, m_ciclos=200, prob_mutacion=0.1, mostrar=True):
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
    
    if mostrar:
        print(f"\nRecorrido Genético (en números): {recorrido_numeros}")
        print(f"Recorrido Genético (en provincias): {recorrido_completo}")
        print(f"Distancia total: {mejor_distancia:.2f}")

    return mejor_recorrido_nombres, mejor_distancia


def ejecutar_corridas_ag(lista_filas, df, n_corridas=10, archivo_salida="corridas_AG.xlsx"):
    resultados = []

    for corrida in range(1, n_corridas + 1):
        recorrido, distancia = resolver_por_ag(lista_filas, df, mostrar=False)

        recorrido_numeros = [lista_filas.index(p) + 1 for p in recorrido]
        recorrido_numeros.append(recorrido_numeros[0])    
        recorrido_nombres = recorrido + [recorrido[0]]

        resultados.append({
            "Corrida": corrida,
            "Distancia (km)": round(distancia, 2),
            "Secuencia (números)": " - ".join(map(str, recorrido_numeros)),
            "Secuencia (provincias)": " - ".join(recorrido_nombres),
        })

        print(f"\nCorrida {corrida}")
        print(f"  Secuencia: {recorrido_numeros}")
        print(f"  Provincias: {recorrido_nombres}")
        print(f"  Distancia total: {distancia:.2f} km")

    tabla = pd.DataFrame(resultados)
    distancias = tabla["Distancia (km)"]

    print("\n=== RESUMEN DE CORRIDAS ===")
    print(f"Mejor corrida : {distancias.min():.2f} km (corrida {distancias.idxmin() + 1})")
    print(f"Peor corrida  : {distancias.max():.2f} km")
    print(f"Promedio      : {distancias.mean():.2f} km")
    print(f"Desv. estándar: {distancias.std():.2f} km")

    tabla.to_excel(archivo_salida, index=False)
    print(f"\nResultados guardados en '{archivo_salida}'")

    return tabla