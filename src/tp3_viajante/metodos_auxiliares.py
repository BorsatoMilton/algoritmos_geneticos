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


def calcular_distancia_total(recorrido, df):
    distancia = 0
    for i in range(len(recorrido)):
        origen = recorrido[i]

        destino = recorrido[(i + 1) % len(recorrido)]
        distancia += df.loc[origen, destino]
    return distancia
 
 
def crear_poblacion_inicial(tam_cromosoma, tam_poblacion):
    poblacion = []
    for _ in range(tam_poblacion):
        cromosoma = list(range(tam_cromosoma))
        random.shuffle(cromosoma)
        poblacion.append(cromosoma)
    return poblacion
 
 
def evaluar_poblacion(poblacion, df, lista_filas):
    fitness = []
    for cromosoma in poblacion:
        recorrido_nombres = [lista_filas[i] for i in cromosoma]
        fitness.append(calcular_distancia_total(recorrido_nombres, df))
    return fitness
 
 
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