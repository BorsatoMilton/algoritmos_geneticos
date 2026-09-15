import pandas as pd
import math
import random

def realizar_recorrido(provincias_visitadas, provincias_restantes, df):
    ultima_provincia = provincias_visitadas[-1]
    distancia = math.inf
    proxima_provincia = None

    for provincia_candidata in provincias_restantes:
        dist_actual = df.loc[ultima_provincia, provincia_candidata]
        
        if dist_actual < distancia and dist_actual != 0 and not math.isnan(dist_actual):
            distancia = dist_actual
            proxima_provincia = provincia_candidata
            
    provincias_visitadas.append(proxima_provincia)
    provincias_restantes.remove(proxima_provincia) 
    
    return provincias_visitadas, provincias_restantes, distancia


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

    
def calcular_distancia_total(recorrido, df):
    distancia = 0
    for i in range(len(recorrido)):
        origen = recorrido[i]

        destino = recorrido[(i + 1) % len(recorrido)]
        distancia += df.loc[origen, destino]
    return distancia
 
 
def crear_poblacion_inicial(lista_ciudades, tam_poblacion):
    poblacion = []
    for _ in range(tam_poblacion):
        cromosoma = lista_ciudades.copy()
        random.shuffle(cromosoma)
        poblacion.append(cromosoma)
    return poblacion
 
 
def evaluar_poblacion(poblacion, df):
    return [calcular_distancia_total(cromosoma, df) for cromosoma in poblacion]
 
 
def seleccion_por_torneo(poblacion, fitness, k=3):
    seleccionados = random.sample(range(len(poblacion)), k)
    mejor = min(seleccionados, key=lambda i: fitness[i])
    return poblacion[mejor].copy()
 
 
def crossover_ciclico(padre1, padre2):
    tam = len(padre1)
    hijo1 = [None] * tam
    hijo2 = [None] * tam
    visitados = [False] * tam
 
    indice = 0
    ciclo = 1
 
    while None in hijo1:
        if visitados[indice]:
            indice = hijo1.index(None)
            ciclo += 1
            continue
 
        if ciclo % 2 != 0:
            hijo1[indice] = padre1[indice]
            hijo2[indice] = padre2[indice]
        else:
            hijo1[indice] = padre2[indice]
            hijo2[indice] = padre1[indice]
 
        visitados[indice] = True
        valor = padre2[indice]
        indice = padre1.index(valor)
 
    return hijo1, hijo2
 
 
def mutar(cromosoma, prob_mutacion=0.1):
    cromosoma = cromosoma.copy()
    if random.random() < prob_mutacion:
        i, j = random.sample(range(len(cromosoma)), 2)
        cromosoma[i], cromosoma[j] = cromosoma[j], cromosoma[i]
    return cromosoma
 
 
def resolver_por_ag(lista_filas, df, n_poblacion=50, m_ciclos=200, prob_mutacion=0.1):
    poblacion = crear_poblacion_inicial(lista_filas, n_poblacion)
 
    mejor_recorrido = None
    mejor_distancia = math.inf
 
    for ciclo in range(m_ciclos):
        fitness = evaluar_poblacion(poblacion, df)
 
        indice_mejor_actual = fitness.index(min(fitness))
        if fitness[indice_mejor_actual] < mejor_distancia:
            mejor_distancia = fitness[indice_mejor_actual]
            mejor_recorrido = poblacion[indice_mejor_actual].copy()
 
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
 

    recorrido_completo = mejor_recorrido + [mejor_recorrido[0]]
    print(f"\nRecorrido (AG): {recorrido_completo}")
    print(f"Distancia total: {mejor_distancia:.2f}")
 
    return mejor_recorrido, mejor_distancia


def main():

    df = pd.read_excel("TablaCapitales.xlsx", index_col=0)
    df = df.iloc[:24, :24]
    df.columns = df.index

    lista_filas = df.index.tolist()

    print("\nMENU")
    print("1. Ingresar Provincia")
    print("2. Recorrido Mínimo")
    print("3. Resolver por AG")
    print("4. Salir")

    decision = int(input("Ingrese una opción: "))
    while decision < 1 or decision > 4:
        print("Opción inválida. Intente nuevamente.")
        decision = int(input("Ingrese una opción: "))

    if decision == 1:
        ingresar_provincia(lista_filas, df)
    elif decision == 2:
        sin_ingresar_provincia(lista_filas, df)
    elif decision == 3:
        resolver_por_ag(lista_filas, df)
    elif decision == 4:
        print("Saliendo del programa...")
        return


if __name__ == "__main__":
    main()