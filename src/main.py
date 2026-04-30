import random

def main():
    # Parametros del algoritmo genetico
    prob_crossover = 0.75
    prob_mutation = 0.05
    poblacion = [] # cromosoma, numero_decimal, fitness
    ciclos = 20
    longitud_cromosoma = 30
    tamanio_poblacion = 10


    for _ in range(tamanio_poblacion):
        cromosoma = [random.randint(0, 1) for _ in range(longitud_cromosoma)]   
        poblacion.append([cromosoma, 0.0, 0.0])
    
    sumatoria = sumatoria_funcion_objetivo(poblacion)

    calcular_fitness(poblacion, sumatoria)



def sumatoria_funcion_objetivo(poblacion):
    sumatoria = 0
    for i in range(len(poblacion)):
        numero_decimal = pasar_a_decimal(poblacion[i][0])
        poblacion[i][1] = numero_decimal
        sumatoria += calcular_funcion_objetivo(numero_decimal)
    return sumatoria

def pasar_a_decimal(cromosoma):
    numero = 0
    for i in range(len(cromosoma)):
        numero += cromosoma[i] * (2 ** (len(cromosoma) - 1 - i))
    return numero

def calcular_fitness(poblacion, sumatoria):
    for i in range(len(poblacion)):
        fitness = calcular_funcion_objetivo(poblacion[i][1]) / sumatoria
        poblacion[i][2] = fitness

def calcular_funcion_objetivo(numero):
    coef = 2**30 - 1
    return (numero/coef)**2


if __name__ == "__main__":
    main()