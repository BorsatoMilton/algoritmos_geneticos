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
    cromosomas_seleccionados = []
    for _ in range(len(poblacion)):
        candidatos = random.sample(poblacion, k)
        mejor = max(candidatos, key=lambda x: x[2])
        cromosomas_seleccionados.append(mejor)
    return cromosomas_seleccionados

# Elitismo: reemplaza los peores de la nueva generación por los mejores de la anterior
def aplicar_elitismo(poblacion_vieja, poblacion_nueva, n_elite=2):
    # Ordenar vieja por fitness descendente
    mejores = sorted(poblacion_vieja, key=lambda x: x[2], reverse=True)[:n_elite]
    # Reemplazar los últimos n_elite de la nueva generación (los peores tras ordenar)
    poblacion_nueva_ordenada = sorted(poblacion_nueva, key=lambda x: x[2], reverse=True)
    poblacion_nueva_ordenada[-n_elite:] = mejores
    return poblacion_nueva_ordenada