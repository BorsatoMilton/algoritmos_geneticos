import random
from condiciones import (ciclos, longitud_cromosoma, tamanio_poblacion)
from operadores import (pasar_a_decimal, calcular_fitness, calcular_crossover,calcular_mutacion, calcular_resultados)
from seleccion import calcular_ruleta, seleccion_torneo, elitismo
import argparse

def parsear_argumentos():
    parser = argparse.ArgumentParser(description="Algoritmo Genético para optimización de función")
    parser.add_argument("--corridas", type=int, default=20, choices=[20, 100, 200], help="Cantidad de veces que se ejecuta el algoritmo completo (default: 20)")
    parser.add_argument("--metodo", type=str, default="ruleta", choices=["ruleta", "torneo", "elitismo"], help="Método de selección: ruleta | torneo | elitismo (default: ruleta)")
    return parser.parse_args()

def ejecutar_corrida(metodo):
    poblacion = []
    mejores_por_poblacion = [] # lista de tuplas (mejor, peor, promedio) por generación
    mejor_cromosoma = None
 
    # Inicializar población aleatoria
    for _ in range(tamanio_poblacion):
        cromosoma = [random.randint(0, 1) for _ in range(longitud_cromosoma)]
        numero_decimal = pasar_a_decimal(cromosoma)
        poblacion.append([cromosoma, numero_decimal, 0.0])
 
    poblacion_descendente = poblacion
 
    # Ciclos = generaciones dentro de esta corrida
    for _ in range(ciclos):
        calcular_fitness(poblacion_descendente)
 
        if metodo == "ruleta":
            cromosomas_seleccionados = calcular_ruleta(poblacion_descendente)
        elif metodo == "torneo":
            cromosomas_seleccionados = seleccion_torneo(poblacion_descendente, k=3)
        elif metodo == "elitismo":
            cromosomas_seleccionados = elitismo(poblacion_descendente)
        
 
        nueva_generacion = calcular_crossover(poblacion_descendente, cromosomas_seleccionados)
        calcular_mutacion(nueva_generacion)
        mejor_cromosoma = calcular_resultados(poblacion_descendente, mejores_por_poblacion, mejor_cromosoma)
        poblacion_descendente = nueva_generacion
 
    return mejores_por_poblacion, mejor_cromosoma



def main():
    args = parsear_argumentos()
    print(f"\n=== Algoritmo Genético | Método: {args.metodo.upper()} | Corridas: {args.corridas} | Ciclos por corrida: {ciclos} ===\n")
 
    resultados_todas_corridas = []   # lista de mejores_por_poblacion de cada corrida
    mejor_cromosoma_global = None
 
    for corrida in range(args.corridas):
        mejores_por_poblacion, mejor_cromosoma = ejecutar_corrida(args.metodo)
        resultados_todas_corridas.append(mejores_por_poblacion)
 
        # Actualizar mejor cromosoma global entre todas las corridas
        if mejor_cromosoma_global is None or mejor_cromosoma[2] > mejor_cromosoma_global[2]:
            mejor_cromosoma_global = mejor_cromosoma
 
        # Imprimir detalle de cada corrida con sus generaciones
        print(f"\n--- Corrida {corrida + 1} ---")
        for i, (mejor, peor, promedio) in enumerate(mejores_por_poblacion):
            print(f"  Generacion {i+1:02d} | "
                  f"Mejor: {mejor[2]:.6f} | "
                  f"Peor: {peor[2]:.6f} | "
                  f"Promedio: {promedio:.6f}")
 
    # ── Resumen final ──────────────────────────────────────────────
    print(f"\n=== RESUMEN FINAL ({args.corridas} corridas) ===")
    print(f"Mejor cromosoma global: {mejor_cromosoma_global[0]}")
    print(f"Valor decimal:          {mejor_cromosoma_global[1]}")
    print(f"Fitness (valor máximo): {mejor_cromosoma_global[2]:.8f}")
 
if __name__ == "__main__":
    main()