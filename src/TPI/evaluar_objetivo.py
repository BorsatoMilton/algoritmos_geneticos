"""
Objetivo 5: Evaluar el desempeño del algoritmo genético en términos de
  - precisión (estabilidad del óptimo entre corridas independientes)
  - tiempo de convergencia (curva de fitness por generación + tiempo real)
  - mejora porcentual de la generación energética respecto de la
    configuración tradicional (inclinación = latitud, azimut = 0)

Genera:
  - resultados_objetivo5.csv      -> una fila por corrida (semilla)
  - convergencia_objetivo5.png    -> curvas de convergencia superpuestas
  - comparacion_ga_vs_trad.png    -> barras GA vs. tradicional (media ± std)
"""

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pvlib
from pvlib.iotools import get_pvgis_tmy

from ga import ejecutar_optimizacion
from funciones import calcular_energia_anual

# ---------------------------------------------------------------
# Configuración del experimento
# ---------------------------------------------------------------
LATITUDE = -32.94
LONGITUDE = -60.63
PERDIDAS_SISTEMA = 0.14
POTENCIA_PICO_KWP = 1.0

POP_SIZE = 20
N_GENERACIONES = 10
N_CORRIDAS = 15          # cantidad de corridas independientes para medir precisión
SEMILLAS = list(range(N_CORRIDAS))


def cargar_datos_clima(latitude, longitude):
    data, meta = get_pvgis_tmy(latitude=latitude, longitude=longitude,
                                usehorizon=True, coerce_year=2025)
    data = data.rename(columns={
        "temp_air": "temperatura_aire",
        "relative_humidity": "humedad_relativa",
        "ghi": "radiacion_global_horizontal",
        "dni": "radiacion_directa_normal",
        "dhi": "radiacion_difusa_horizontal",
        "IR(h)": "radiacion_infrarroja",
        "wind_speed": "velocidad_viento",
        "wind_direction": "direccion_viento",
        "pressure": "presion",
    })

    sol = pvlib.solarposition.get_solarposition(
        time=data.index, latitude=latitude, longitude=longitude
    )
    dni_extra = pvlib.irradiance.get_extra_radiation(data.index)
    airmass = pvlib.atmosphere.get_relative_airmass(sol['apparent_zenith'])

    return data, sol, dni_extra, airmass


def main():
    print(f"Descargando/generando TMY para lat={LATITUDE}, lon={LONGITUDE}...")
    datos_clima, sol, dni_extra, airmass = cargar_datos_clima(LATITUDE, LONGITUDE)

    # Línea base: método tradicional (inclinación = |latitud|, azimut = 0)
    angulos_tradicionales = [abs(LATITUDE), 0.0]
    energia_tradicional = calcular_energia_anual(
        angulos_tradicionales, datos_clima, sol, dni_extra, airmass,
        PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
    )
    print(f"Energía método tradicional: {energia_tradicional:.2f} kWh/año\n")

    resultados = []
    historiales = []

    t_experimento_inicio = time.time()

    for i, seed in enumerate(SEMILLAS):
        print(f"--- Corrida {i+1}/{N_CORRIDAS} (semilla={seed}) ---")
        mejor_individuo, historial, tiempo_corrida = ejecutar_optimizacion(
            datos_clima, sol, dni_extra, airmass,
            pop_size=POP_SIZE, n_generaciones=N_GENERACIONES,
            perdidas_sistema=PERDIDAS_SISTEMA, potencia_pico_kwp=POTENCIA_PICO_KWP,
            seed=seed, verbose=False
        )

        energia_optimizada = calcular_energia_anual(
            mejor_individuo, datos_clima, sol, dni_extra, airmass,
            PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
        )
        ganancia_pct = ((energia_optimizada - energia_tradicional) / energia_tradicional) * 100

        # Generación en la que se alcanza el 99% del valor final (proxy de convergencia)
        umbral = 0.99 * historial[-1]
        gen_convergencia = next(
            (g for g, v in enumerate(historial) if v >= umbral), len(historial) - 1
        )

        resultados.append({
            "semilla": seed,
            "inclinacion_opt": mejor_individuo[0],
            "azimut_opt": mejor_individuo[1],
            "energia_optimizada_kwh": energia_optimizada,
            "ganancia_pct_vs_tradicional": ganancia_pct,
            "tiempo_corrida_seg": tiempo_corrida,
            "generacion_convergencia_99pct": gen_convergencia,
        })
        historiales.append(historial)

        print(f"  Tilt={mejor_individuo[0]:.2f}°  Azim={mejor_individuo[1]:.2f}°  "
              f"Energía={energia_optimizada:.2f} kWh  Mejora={ganancia_pct:.2f}%  "
              f"Tiempo={tiempo_corrida:.1f}s  ConvGen={gen_convergencia}")

    tiempo_experimento_total = time.time() - t_experimento_inicio

    df = pd.DataFrame(resultados)
    df.to_csv("resultados_objetivo5.csv", index=False)

    # -----------------------------------------------------------
    # Estadísticas de PRECISIÓN (estabilidad entre corridas)
    # -----------------------------------------------------------
    print("\n=== RESUMEN OBJETIVO 5 ===")
    print(f"Corridas independientes: {N_CORRIDAS}")
    print(f"Tiempo total del experimento: {tiempo_experimento_total/60:.1f} min\n")

    print("--- Precisión (media ± desvío estándar entre corridas) ---")
    print(f"Inclinación óptima : {df['inclinacion_opt'].mean():.2f}° ± {df['inclinacion_opt'].std():.2f}°")
    print(f"Azimut óptimo      : {df['azimut_opt'].mean():.2f}°  ± {df['azimut_opt'].std():.2f}°")
    print(f"Energía optimizada : {df['energia_optimizada_kwh'].mean():.2f} ± {df['energia_optimizada_kwh'].std():.2f} kWh/año")
    print(f"Mejora vs. tradic. : {df['ganancia_pct_vs_tradicional'].mean():.2f}% ± {df['ganancia_pct_vs_tradicional'].std():.2f}%")

    print("\n--- Tiempo de convergencia ---")
    print(f"Tiempo por corrida : {df['tiempo_corrida_seg'].mean():.1f}s ± {df['tiempo_corrida_seg'].std():.1f}s")
    print(f"Generación conv.(99%): {df['generacion_convergencia_99pct'].mean():.1f} ± {df['generacion_convergencia_99pct'].std():.1f} de {N_GENERACIONES}")

    # -----------------------------------------------------------
    # Gráfico 1: curvas de convergencia superpuestas
    # -----------------------------------------------------------
    plt.figure(figsize=(9, 5))
    for h in historiales:
        plt.plot(h, alpha=0.35, color="steelblue")
    historial_promedio = np.mean(historiales, axis=0)
    plt.plot(historial_promedio, color="navy", linewidth=2.5, label="Promedio de corridas")
    plt.axhline(energia_tradicional, color="red", linestyle="--", label="Método tradicional")
    plt.xlabel("Generación")
    plt.ylabel("Mejor energía anual (kWh)")
    plt.title(f"Convergencia del GA ({N_CORRIDAS} corridas independientes)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("convergencia_objetivo5.png", dpi=150)
    plt.close()

    # -----------------------------------------------------------
    # Gráfico 2: comparación GA vs. tradicional (barras con error)
    # -----------------------------------------------------------
    plt.figure(figsize=(5, 5))
    medias = [energia_tradicional, df['energia_optimizada_kwh'].mean()]
    errores = [0, df['energia_optimizada_kwh'].std()]
    plt.bar(["Tradicional\n(β=lat, γ=0°)", "GA\n(óptimo)"], medias,
            yerr=errores, capsize=8, color=["gray", "seagreen"])
    plt.ylabel("Energía anual (kWh)")
    plt.title("Comparación: GA vs. método tradicional")
    for i, v in enumerate(medias):
        plt.text(i, v + max(medias) * 0.01, f"{v:.0f}", ha="center")
    plt.tight_layout()
    plt.savefig("comparacion_ga_vs_trad.png", dpi=150)
    plt.close()

    print("\nArchivos generados:")
    print("  - resultados_objetivo5.csv")
    print("  - convergencia_objetivo5.png")
    print("  - comparacion_ga_vs_trad.png")


if __name__ == "__main__":
    main()