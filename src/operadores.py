import random
from condiciones import prob_crossover, prob_mutacion

def pasar_a_decimal(cromosoma):
    numero = 0
    for i in range(len(cromosoma)):
        numero += cromosoma[i] * (2 ** (len(cromosoma) - 1 - i))
    return numero

def calcular_funcion_objetivo(numero):
    coef = 2**30 - 1
    return (numero/coef)**2

def sumatoria_funcion_objetivo(poblacion):
    sumatoria = 0
    for i in range(len(poblacion)):
        sumatoria += calcular_funcion_objetivo(poblacion[i][1])
    return sumatoria

def calcular_fitness(poblacion):
    sumatoria = sumatoria_funcion_objetivo(poblacion)
    for i in range(len(poblacion)):
        fitness = calcular_funcion_objetivo(poblacion[i][1]) / sumatoria
        poblacion[i][2] = fitness

def calcular_crossover(poblacion, lista_cromosomas_seleccionados):
    nueva_generacion = []
    for i in range(0, len(lista_cromosomas_seleccionados), 2):
        numero_aleatorio = random.random()
        if numero_aleatorio <= prob_crossover:
            punto_corte = random.randint(1, len(poblacion[i][0]) - 1)
            hijo_1 = lista_cromosomas_seleccionados[i][0][:punto_corte] + lista_cromosomas_seleccionados[i+1][0][punto_corte:]
            hijo_2 = lista_cromosomas_seleccionados[i+1][0][:punto_corte] + lista_cromosomas_seleccionados[i][0][punto_corte:]
            nueva_generacion.append([hijo_1, pasar_a_decimal(hijo_1), 0.0])
            nueva_generacion.append([hijo_2, pasar_a_decimal(hijo_2), 0.0])
        else:
            nueva_generacion.append(lista_cromosomas_seleccionados[i])
            nueva_generacion.append(lista_cromosomas_seleccionados[i+1])
    return nueva_generacion

def calcular_mutacion(nueva_generacion):
    for i in range(len(nueva_generacion)):
        numero_aleatorio = random.random()
        if numero_aleatorio <= prob_mutacion:
            punto_mutacion = random.randint(0, len(nueva_generacion[i][0]) - 1)
            nueva_generacion[i][0][punto_mutacion] = 1 - nueva_generacion[i][0][punto_mutacion]
            nueva_generacion[i][1] = pasar_a_decimal(nueva_generacion[i][0])

def calcular_resultados(poblacion, mejores_por_poblacion, mejor_cromosoma):
    mejor_cromosoma_poblacion = max(poblacion, key=lambda x: calcular_funcion_objetivo(x[1]))
    peor_cromosoma_poblacion = min(poblacion, key=lambda x: calcular_funcion_objetivo(x[1]))
    promedio_cromosomas_poblacion = sum(calcular_funcion_objetivo(poblacion[i][1]) for i in range(len(poblacion))) / len(poblacion)
    if mejor_cromosoma is None or calcular_funcion_objetivo(mejor_cromosoma_poblacion[1]) > calcular_funcion_objetivo(mejor_cromosoma[1]):
        mejor_cromosoma = mejor_cromosoma_poblacion
    mejores_por_poblacion.append([mejor_cromosoma_poblacion, peor_cromosoma_poblacion, promedio_cromosomas_poblacion])
    return mejor_cromosoma