import random

def main():
    # Parametros del algoritmo genetico
    prob_crossover = 0.75
    prob_mutation = 0.05
    poblacion_inicial = [] # cromosoma, numero_decimal, fitness
    ciclos = 20
    longitud_cromosoma = 30
    tamanio_poblacion = 10

    # Parametros resultados
    mejores_por_poblacion = [] # lista de los mejores cromosomas por cada descendencia (mejor, menor, promedio)
    mejor_cromosoma = None # mejor cromosoma encontrado en todo el proceso


    for _ in range(tamanio_poblacion):
        cromosoma = [random.randint(0, 1) for _ in range(longitud_cromosoma)]   
        numero_decimal = pasar_a_decimal(cromosoma)
        poblacion_inicial.append([cromosoma, numero_decimal, 0.0])
    

    poblacion_descendente = poblacion_inicial

    for i in range(ciclos):

        calcular_fitness(poblacion_descendente)

        cromosomas_seleccionados = calcular_ruleta(poblacion_descendente)

        nueva_generacion = calcular_crossover(poblacion_descendente, prob_crossover, cromosomas_seleccionados)

        calcular_mutacion(nueva_generacion, prob_mutation)

        mejor_cromosoma = calcular_resultados(poblacion_descendente, mejores_por_poblacion, mejor_cromosoma)

        poblacion_descendente = nueva_generacion


        print("__________________________________")
        print(f"Generacion: {i + 1}")
        print(f"Mejor cromosoma poblacion: {mejores_por_poblacion[i][0][0]} - Numero decimal: {mejores_por_poblacion[i][0][1]} - Fitness: {mejores_por_poblacion[i][0][2]}")
        print(f"Peor cromosoma poblacion: {mejores_por_poblacion[i][1][0]} - Numero decimal: {mejores_por_poblacion[i][1][1]} - Fitness: {mejores_por_poblacion[i][1][2]}")
        print(f"Promedio cromosomas poblacion: {mejores_por_poblacion[i][2]}")

    print(f"Mejor cromosoma total: {mejor_cromosoma[0]} - Numero decimal: {mejor_cromosoma[1]} - Fitness: {mejor_cromosoma[2]}")


def calcular_ruleta(poblacion):
    lista_ruleta = [] # lista que tiene los fitness sumados, para generar intervalos de la ruleta
    lista_cromosomas_seleccionados = [] # lista de cromosomas seleccionados para el crossover
    
    for i in range(len(poblacion)):
        lista_ruleta.append(poblacion[i][2] + (lista_ruleta[i-1] if i > 0 else 0))

    for i in range(len(poblacion)):
        numero_aleatorio = random.random()
        for j in range(len(lista_ruleta)):
            if numero_aleatorio < lista_ruleta[j]:
                lista_cromosomas_seleccionados.append(poblacion[j])
                break
    return lista_cromosomas_seleccionados
    

def calcular_crossover(poblacion, prob_crossover, lista_cromosomas_seleccionados):
    nueva_generacion = [] # lista de cromosomas resultantes del crossover y mutacion
    
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


def calcular_mutacion(nueva_generacion, prob_mutation):
    for i in range(len(nueva_generacion)):
        numero_aleatorio = random.random()
        if numero_aleatorio <= prob_mutation:
            punto_mutacion = random.randint(0, len(nueva_generacion[i][0]) - 1)
            nueva_generacion[i][0][punto_mutacion] = 1 - nueva_generacion[i][0][punto_mutacion]
            nueva_generacion[i][1] = pasar_a_decimal(nueva_generacion[i][0])


def calcular_fitness(poblacion):
    sumatoria = sumatoria_funcion_objetivo(poblacion)

    for i in range(len(poblacion)):
        fitness = calcular_funcion_objetivo(poblacion[i][1]) / sumatoria
        poblacion[i][2] = fitness


def calcular_funcion_objetivo(numero):
    coef = 2**30 - 1
    return (numero/coef)**2


def calcular_resultados(poblacion, mejores_por_poblacion, mejor_cromosoma):
    mejor_cromosoma_poblacion = max(poblacion, key=lambda x: calcular_funcion_objetivo(x[1]))
    peor_cromosoma_poblacion = min(poblacion, key=lambda x: calcular_funcion_objetivo(x[1]))
    promedio_cromosomas_poblacion = sum(calcular_funcion_objetivo(poblacion[i][1]) for i in range(len(poblacion))) / len(poblacion)


    if mejor_cromosoma is None or calcular_funcion_objetivo(mejor_cromosoma_poblacion[1]) > calcular_funcion_objetivo(mejor_cromosoma[1]):
        mejor_cromosoma = mejor_cromosoma_poblacion

    mejores_por_poblacion.append([mejor_cromosoma_poblacion, peor_cromosoma_poblacion, promedio_cromosomas_poblacion])

    return mejor_cromosoma
    


def sumatoria_funcion_objetivo(poblacion):
    sumatoria = 0
    for i in range(len(poblacion)):
        sumatoria += calcular_funcion_objetivo(poblacion[i][1])
    return sumatoria


def pasar_a_decimal(cromosoma):
    numero = 0
    for i in range(len(cromosoma)):
        numero += cromosoma[i] * (2 ** (len(cromosoma) - 1 - i))
    return numero


if __name__ == "__main__":
    main()