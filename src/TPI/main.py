from ga import ejecutar_optimizacion
from funciones import calcular_energia_anual
from config import (
    cargar_datos_clima, ANGULOS_TRADICIONALES,
    PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
)

POP_SIZE = 50
N_GENERACIONES = 20


def main():
    print("Descargando/generando TMY...")
    datos_clima, sol, dni_extra, airmass = cargar_datos_clima()

    mejor_config, historial, tiempo = ejecutar_optimizacion(
        datos_clima, sol, dni_extra, airmass,
        pop_size=POP_SIZE, n_generaciones=N_GENERACIONES,
        perdidas_sistema=PERDIDAS_SISTEMA, potencia_pico_kwp=POTENCIA_PICO_KWP,
        seed=42, verbose=True
    )

    energia_tradicional = calcular_energia_anual(
        ANGULOS_TRADICIONALES, datos_clima, sol, dni_extra, airmass,
        PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
    )
    energia_optimizada = calcular_energia_anual(
        mejor_config, datos_clima, sol, dni_extra, airmass,
        PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
    )

    ganancia_porcentaje = ((energia_optimizada - energia_tradicional) / energia_tradicional) * 100

    print(f"\n--- COMPARACIÓN GA vs. TRADICIONAL ---")
    print(f"Energía método tradicional ({ANGULOS_TRADICIONALES[0]:.2f}°, {ANGULOS_TRADICIONALES[1]:.2f}°): {energia_tradicional:.2f} kWh/año")
    print(f"Energía método optimizado  ({mejor_config[0]:.2f}°, {mejor_config[1]:.2f}°): {energia_optimizada:.2f} kWh/año")
    print(f"Mejora conseguida con GA: {ganancia_porcentaje:.2f}%")
    print(f"Tiempo de ejecución: {tiempo:.2f}s")


if __name__ == "__main__":
    main()