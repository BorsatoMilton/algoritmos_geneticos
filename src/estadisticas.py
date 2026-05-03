from operadores import calcular_funcion_objetivo
import statistics
import time

#Desviacion estandar de FITNESS de cada GENERACION
def calcular_desviacion_estandar(poblacion):
    fitness_valores = [individuo[2] for individuo in poblacion]
    return statistics.stdev(fitness_valores) if len(fitness_valores) > 1 else 0 # Si solo hay un individuo, la desviación estándar es 0

def medir_tiempo(func, *args, **kwargs):

    inicio = time.perf_counter()
    resultado = func(*args, **kwargs) #sirve para almacenar el resultado de la función que se está midiendo. Se quiere almacenar el resultado para poder devolverlo junto con el tiempo de ejecución. Esto es útil porque a menudo queremos no solo saber cuánto tiempo tarda una función en ejecutarse, sino también obtener el resultado que produce esa función para su posterior uso o análisis.
    fin = time.perf_counter()
    return resultado, fin - inicio

def calcular_resultados(poblacion, mejores_por_poblacion, mejor_cromosoma):
    mejor_cromosoma_poblacion = max(poblacion, key=lambda x: calcular_funcion_objetivo(x[1]))
    peor_cromosoma_poblacion = min(poblacion, key=lambda x: calcular_funcion_objetivo(x[1]))
    #promedio_cromosomas_poblacion = sum(calcular_funcion_objetivo(poblacion[i][1]) for i in range(len(poblacion))) / len(poblacion)
    promedio_cromosomas_poblacion = statistics.mean(calcular_funcion_objetivo(poblacion[i][1]) for i in range(len(poblacion)))
    desviacion_estandar_fitness = calcular_desviacion_estandar(poblacion)
    
    if mejor_cromosoma is None or calcular_funcion_objetivo(mejor_cromosoma_poblacion[1]) > calcular_funcion_objetivo(mejor_cromosoma[1]):
        mejor_cromosoma = mejor_cromosoma_poblacion
    mejores_por_poblacion.append([mejor_cromosoma_poblacion, peor_cromosoma_poblacion, promedio_cromosomas_poblacion, desviacion_estandar_fitness])

    return mejor_cromosoma