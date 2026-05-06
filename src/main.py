import random
import statistics
from variables_globales import (longitud_cromosoma, tamanio_poblacion, corridas)
from funciones_auxiliares import (pasar_a_decimal, calcular_fitness, calcular_crossover,calcular_mutacion, calcular_funcion_objetivo, calcular_desviacion_estandar_fitness, calcular_resultados)
from metodos_seleccion import calcular_ruleta, seleccion_torneo, elitismo
import argparse
import time


class impresion_tablas:
    def __init__(self):
        self.minimos = {20:None, 100:None, 200:None}
        self.maximos = {20:None, 100:None, 200:None}
        self.promedios = {20:None, 100:None, 200:None}
        self.desviacion_estandar_fitness = {20:None, 100:None, 200:None}
        self.tiempos_de_ejecucion = {20:None, 100:None, 200:None}


def main():
    args = parsear_argumentos()
    print(f"\n=== Algoritmo Genético | Método: {args.metodo.upper()} | ===\n")
 
    tabla_impresion = impresion_tablas()

    poblacion_inicial = generar_poblacion_inicial()
    
    for cant_corridas in corridas:

        tiempo_inicio = time.perf_counter()

        maximo_por_corrida = []
        minimo_por_corrida = []
        promedio_por_corrida = []
        desviacion_estandar_fitness_por_corrida = []

        maximo_por_corrida.append([0,max(poblacion_inicial, key=lambda x: calcular_funcion_objetivo(x[1]))])
        minimo_por_corrida.append([0,min(poblacion_inicial, key=lambda x: calcular_funcion_objetivo(x[1]))])
        promedio_por_corrida.append([0,statistics.mean(calcular_funcion_objetivo(x[1]) for x in poblacion_inicial)])
        desviacion_estandar_fitness_por_corrida.append([0,statistics.stdev(calcular_funcion_objetivo(x[1]) for x in poblacion_inicial)])

        poblacion_descendente = poblacion_inicial.copy()

        for corrida in range(cant_corridas - 1): # -1 porque la poblacion inicial ya se cuenta como una corrida

            nueva_generacion, mejor_cromosoma, peor_cromosoma, promedio, desviacion_estandar_fitness = ejecutar_corrida(args.metodo, poblacion_descendente)


            maximo_por_corrida.append([corrida+1,mejor_cromosoma])
            minimo_por_corrida.append([corrida+1,peor_cromosoma])
            promedio_por_corrida.append([corrida+1,promedio])
            desviacion_estandar_fitness_por_corrida.append([corrida+1,desviacion_estandar_fitness])


            if tabla_impresion.maximos[cant_corridas] is None or calcular_funcion_objetivo(mejor_cromosoma[1]) > calcular_funcion_objetivo(tabla_impresion.maximos[cant_corridas][1]):
                tabla_impresion.maximos[cant_corridas] = mejor_cromosoma

            if tabla_impresion.minimos[cant_corridas] is None or calcular_funcion_objetivo(peor_cromosoma[1]) < calcular_funcion_objetivo(tabla_impresion.minimos[cant_corridas][1]):
                tabla_impresion.minimos[cant_corridas] = peor_cromosoma

            poblacion_descendente = nueva_generacion
    
        tabla_impresion.promedios[cant_corridas] = statistics.mean(promedio_por_corrida[i][1] for i in range(len(promedio_por_corrida))) #promedio de los promedios de esta corrida
        tabla_impresion.desviacion_estandar_fitness[cant_corridas] = statistics.mean(desviacion_estandar_fitness_por_corrida[i][1] for i in range(len(desviacion_estandar_fitness_por_corrida))) #promedio de las desviaciones estandar de esta corrida

        tabla_impresion.tiempos_de_ejecucion[cant_corridas] = time.perf_counter() - tiempo_inicio


    print("Resultados por cantidad de corridas:")
    for cant_corridas in corridas:
        print("______________________________________")
        print(f"\nCorridas: {cant_corridas}")
        print(f"Mejor cromosoma: {tabla_impresion.maximos[cant_corridas]} \nPeor cromosoma: {tabla_impresion.minimos[cant_corridas]} \nPromedio: {tabla_impresion.promedios[cant_corridas]:.6f} \nDesviación estándar del fitness: {tabla_impresion.desviacion_estandar_fitness[cant_corridas]:.6f} \nTiempo de ejecución: {tabla_impresion.tiempos_de_ejecucion[cant_corridas]:.6f} segundos")
    
    # FALTAN GRÁFICAS   


def ejecutar_corrida(metodo, poblacion):

    if metodo == "ruleta":
        funcion_seleccion = calcular_ruleta
    elif metodo == "torneo":
        funcion_seleccion = lambda poblacion: seleccion_torneo(poblacion, k=3)
    elif metodo == "elitismo":
        funcion_seleccion = elitismo
    
    if metodo == "elitismo":
        elite = elitismo(poblacion) # Recordar que se puede variar el K, esta hardcodeado a 2 por el cvg

    cromosomas_seleccionados = funcion_seleccion(poblacion)
    nueva_generacion = calcular_crossover(poblacion, cromosomas_seleccionados)
    calcular_mutacion(nueva_generacion)

    calcular_fitness(nueva_generacion)

    if metodo == "elitismo":
        nueva_generacion.sort(key=lambda x: x[2])
        nueva_generacion[:len(elite)] = elite

    mejor_cromosoma, peor_cromosoma, promedio, desviacion_estandar_fitness = calcular_resultados(nueva_generacion)

    for individuo in nueva_generacion:
        individuo[3] = desviacion_estandar_fitness

    return nueva_generacion, mejor_cromosoma, peor_cromosoma, promedio, desviacion_estandar_fitness


def generar_poblacion_inicial():
    poblacion_inicial = [] # cromosoma, numero_decimal, fitness, desviacion_estandar_fitness
    for _ in range(tamanio_poblacion):
        cromosoma = [random.randint(0, 1) for _ in range(longitud_cromosoma)]
        numero_decimal = pasar_a_decimal(cromosoma)
        poblacion_inicial.append([cromosoma, numero_decimal, 0.0, 0.0]) #cromosoma, numero_decimal, fitness, desviacion_estandar_fitness
    
    calcular_fitness(poblacion_inicial)

    desviacion_estandar_fitness = calcular_desviacion_estandar_fitness(poblacion_inicial)

    for individuo in poblacion_inicial:
        individuo[3] = desviacion_estandar_fitness

    return poblacion_inicial


def parsear_argumentos():
    parser = argparse.ArgumentParser(description="Algoritmo Genético para optimización de función")
    parser.add_argument("--metodo", type=str, default="ruleta", choices=["ruleta", "torneo", "elitismo"], help="Método de selección: ruleta | torneo | elitismo (default: ruleta)")
    return parser.parse_args()


if __name__ == "__main__":
    main()