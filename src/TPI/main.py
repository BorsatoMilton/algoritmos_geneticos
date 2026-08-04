from ga import ejecutar_optimizacion
from funciones import calcular_energia_anual
from evaluar_objetivo import (
    cargar_datos_clima, LATITUDE, LONGITUDE,
    PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
)

# Configuración elegida según el barrido de hiperparámetros (ver
# barrido_hiperparametros.py): pop_size=50 / n_generaciones=20 da
# prácticamente la misma calidad que 100/30 con ~3x menos tiempo de cómputo.
POP_SIZE = 50
N_GENERACIONES = 20


def main():
    print(f"Descargando/generando TMY para lat={LATITUDE}, lon={LONGITUDE}...")
    datos_clima, sol, dni_extra, airmass = cargar_datos_clima(LATITUDE, LONGITUDE)

    mejor_config, historial, tiempo = ejecutar_optimizacion(
        datos_clima, sol, dni_extra, airmass,
        pop_size=POP_SIZE, n_generaciones=N_GENERACIONES,
        perdidas_sistema=PERDIDAS_SISTEMA, potencia_pico_kwp=POTENCIA_PICO_KWP,
        seed=42, verbose=True
    )

    angulos_tradicionales = [abs(LATITUDE), 0.0]
    energia_tradicional = calcular_energia_anual(
        angulos_tradicionales, datos_clima, sol, dni_extra, airmass,
        PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
    )
    energia_optimizada = calcular_energia_anual(
        mejor_config, datos_clima, sol, dni_extra, airmass,
        PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
    )

    ganancia_porcentaje = ((energia_optimizada - energia_tradicional) / energia_tradicional) * 100

    print(f"\n--- COMPARACIÓN GA vs. TRADICIONAL ---")
    print(f"Energía método tradicional ({angulos_tradicionales[0]:.2f}°, {angulos_tradicionales[1]:.2f}°): {energia_tradicional:.2f} kWh/año")
    print(f"Energía método optimizado  ({mejor_config[0]:.2f}°, {mejor_config[1]:.2f}°): {energia_optimizada:.2f} kWh/año")
    print(f"Mejora conseguida con GA: {ganancia_porcentaje:.2f}%")
    print(f"Tiempo de ejecución: {tiempo:.2f}s")


if __name__ == "__main__":
    main()