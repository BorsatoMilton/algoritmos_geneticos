import random

def calcular_ruleta(poblacion):
    lista_ruleta = []
    lista_cromosomas_seleccionados = []
    for i in range(len(poblacion)):
        lista_ruleta.append(poblacion[i][2] + (lista_ruleta[i-1] if i > 0 else 0))
    
    lista_ruleta[-1] = 1.0 # Asegurar que el último valor sea exactamente 1 para evitar problemas de precisión
    
    for i in range(len(poblacion)):
        numero_aleatorio = random.random()
        for j in range(len(lista_ruleta)):
            if numero_aleatorio <= lista_ruleta[j]:
                seleccionado = poblacion[j]
                break
        lista_cromosomas_seleccionados.append(seleccionado)
    return lista_cromosomas_seleccionados

# Función torneo (k=3 por defecto)
def seleccion_torneo(poblacion, k=3):
    lista_cromosomas_seleccionados = []
    for i in range(len(poblacion)):
        candidatos = random.sample(poblacion, k)
        mejor = max(candidatos, key=lambda x: x[2])
        lista_cromosomas_seleccionados.append(mejor)
    return lista_cromosomas_seleccionados

# Elitismo
def elitismo(poblacion, cant_elite=2):
    poblacion_ordenada = sorted(poblacion, key=lambda x: x[2], reverse=True)
    return poblacion_ordenada[:cant_elite]
    