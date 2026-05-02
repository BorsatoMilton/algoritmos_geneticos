import random

def calcular_ruleta(poblacion):
    lista_ruleta = []
    lista_cromosomas_seleccionados = []
    for i in range(len(poblacion)):
        lista_ruleta.append(poblacion[i][2] + (lista_ruleta[i-1] if i > 0 else 0))
    for i in range(len(poblacion)):
        numero_aleatorio = random.random()
        for j in range(len(lista_ruleta)):
            if numero_aleatorio < lista_ruleta[j]:
                lista_cromosomas_seleccionados.append(poblacion[j])
                break
    return lista_cromosomas_seleccionados

# Función torneo (k=3 por defecto)
def seleccion_torneo(poblacion, k=3):
    lista_cromosomas_seleccionados = []
    for i in range(len(poblacion)):
        # Elegir k candidatos aleatorios
        candidatos = random.sample(poblacion, k)
        # Elegir el mejor por fitness (índice 2 de cada individuo)
        mejor = max(candidatos, key=lambda x: x[2])
        lista_cromosomas_seleccionados.append(mejor)
    return lista_cromosomas_seleccionados

# Elitismo
def elitismo(poblacion):
    # Ordenar la poblacion por fitness de mayor a menor
    poblacion_ordenada = sorted(poblacion, key=lambda x: x[2], reverse=True)
    # Seleccionar los mejores (elitismo) -> el 10% de la poblacion
    numero_de_mejores = max(1, int(len(poblacion) * 0.10))
    mejores = poblacion_ordenada[:numero_de_mejores]
    # Completar el resto de la lista con seleccion por torneo
    restantes = len(poblacion) - numero_de_mejores
    for _ in range(restantes):
        candidatos = random.sample(poblacion, min(3, len(poblacion)))
        mejor = max(candidatos, key=lambda x: x[2])
        mejores.append(mejor)
    # Asegurar que la cantidad sea par para el crossover
    if len(mejores) % 2 != 0:
        candidatos = random.sample(poblacion, min(3, len(poblacion)))
        mejor = max(candidatos, key=lambda x: x[2])
        mejores.append(mejor)
    return mejores
    
    