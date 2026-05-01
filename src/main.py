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
        numero_decimal = pasar_a_decimal(cromosoma)
        poblacion.append([cromosoma, numero_decimal, 0.0])
    
    sumatoria = sumatoria_funcion_objetivo(poblacion)

    calcular_fitness(poblacion, sumatoria)


    cromosomas_seleccionados =calcular_ruleta(poblacion)

    calcular_crossover(poblacion, prob_crossover, cromosomas_seleccionados)













def calcular_ruleta(poblacion):
    lista_ruleta = [] # lista que tiene los fitness sumados, para generar intervalos de la ruleta
    lista_cromosomas_seleccionados = [] # lista de cromosomas seleccionados para el crossover
    
    for i in range(len(poblacion)):
        lista_ruleta.append(poblacion[i][2] + (lista_ruleta[i-1] if i > 0 else 0))

    for i in range(len(poblacion)):
        numero_aleatorio = random.randint(0,1)
        for j in range(len(lista_ruleta)):
            if numero_aleatorio < lista_ruleta[j]:
                lista_cromosomas_seleccionados.append(poblacion[j][0])
                break
    return lista_cromosomas_seleccionados
    

def calcular_crossover(poblacion, prob_crossover, lista_cromosomas_seleccionados):
    nueva_generacion = [] # lista de cromosomas resultantes del crossover y mutacion
    
    for i in range(0, len(lista_cromosomas_seleccionados), 2):
        numero_aleatorio = random.randint(0,1)
        if numero_aleatorio < prob_crossover:
            punto_corte = random.randint(1, len(poblacion[i][0]) - 1)
            hijo_1 = lista_cromosomas_seleccionados[i][:punto_corte] + lista_cromosomas_seleccionados[i+1][punto_corte:]
            hijo_2 = lista_cromosomas_seleccionados[i+1][:punto_corte] + lista_cromosomas_seleccionados[i][punto_corte:]
            nueva_generacion.append(hijo_1)
            nueva_generacion.append(hijo_2)
        else:
            nueva_generacion.append(lista_cromosomas_seleccionados[i])
            nueva_generacion.append(lista_cromosomas_seleccionados[i+1])
    print(nueva_generacion)


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


def calcular_fitness(poblacion, sumatoria):
    for i in range(len(poblacion)):
        fitness = calcular_funcion_objetivo(poblacion[i][1]) / sumatoria
        poblacion[i][2] = fitness


def calcular_funcion_objetivo(numero):
    coef = 2**30 - 1
    return (numero/coef)**2


if __name__ == "__main__":
    main()