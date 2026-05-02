import random
from condiciones import (ciclos, longitud_cromosoma, tamanio_poblacion)
from operadores import (pasar_a_decimal, calcular_fitness, calcular_crossover,calcular_mutacion, calcular_resultados)
from seleccion import calcular_ruleta

def main():
    poblacion_inicial = []
    mejores_por_poblacion = []
    mejor_cromosoma = None

    for _ in range(tamanio_poblacion):
        cromosoma = [random.randint(0, 1) for _ in range(longitud_cromosoma)]
        numero_decimal = pasar_a_decimal(cromosoma)
        poblacion_inicial.append([cromosoma, numero_decimal, 0.0])

    poblacion_descendente = poblacion_inicial

    for i in range(ciclos):
        calcular_fitness(poblacion_descendente)
        
        cromosomas_seleccionados = calcular_ruleta(poblacion_descendente) # selecciona los cromosomas para crossover usando ruleta
        
        nueva_generacion = calcular_crossover(poblacion_descendente, cromosomas_seleccionados) # realiza crossover para generar nueva generación
        
        calcular_mutacion(nueva_generacion) # aplica mutación a la nueva generación
        
        mejor_cromosoma = calcular_resultados(poblacion_descendente, mejores_por_poblacion, mejor_cromosoma)
        
        poblacion_descendente = nueva_generacion

        print("__________________________________")
        print(f"Generacion: {i + 1}")
        print(f"Mejor cromosoma poblacion: {mejores_por_poblacion[i][0][0]} - Numero decimal: {mejores_por_poblacion[i][0][1]} - Fitness: {mejores_por_poblacion[i][0][2]}")
        print(f"Peor cromosoma poblacion: {mejores_por_poblacion[i][1][0]} - Numero decimal: {mejores_por_poblacion[i][1][1]} - Fitness: {mejores_por_poblacion[i][1][2]}")
        print(f"Promedio cromosomas poblacion: {mejores_por_poblacion[i][2]}")

    print(f"Mejor cromosoma total: {mejor_cromosoma[0]} - Numero decimal: {mejor_cromosoma[1]} - Fitness: {mejor_cromosoma[2]}")

if __name__ == "__main__":
    main()