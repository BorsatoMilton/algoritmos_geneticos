import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ga import ejecutar_optimizacion
from funciones import calcular_energia_anual
from config import cargar_datos_clima, ANGULOS_TRADICIONALES, PERDIDAS_SISTEMA, POTENCIA_PICO_KWP

POP_SIZE = 50
N_GENERACIONES = 20
N_CORRIDAS = 15          # cantidad de corridas independientes para medir precisión
SEMILLAS = list(range(N_CORRIDAS))
carpeta_resultados = "graficos"
os.makedirs(carpeta_resultados, exist_ok=True)

def main():
    print("Descargando/generando TMY...")
    datos_clima, sol, dni_extra, airmass = cargar_datos_clima()

    energia_tradicional = calcular_energia_anual(
        ANGULOS_TRADICIONALES, datos_clima, sol, dni_extra, airmass,
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

        umbral = 0.99 * historial[-1]
        gen_convergencia = len(historial) - 1

        for g, v in enumerate(historial):
            if v >= umbral:
                gen_convergencia = g
                break

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

    carpeta_resultados = "graficos"
    os.makedirs(carpeta_resultados, exist_ok=True)

    df = pd.DataFrame(resultados)
    ruta_csv = os.path.join(carpeta_resultados, "resultados_objetivo5.csv")
    df.to_csv(ruta_csv, index=False)
    

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
    ruta_archivo = os.path.join(carpeta_resultados, "convergencia_objetivo5.png")
    plt.savefig(ruta_archivo, dpi=150)
    plt.close()


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
    ruta_archivo = os.path.join(carpeta_resultados, "comparacion_ga_vs_trad.png")
    plt.savefig(ruta_archivo, dpi=150)
    plt.close()

    print("\nArchivos generados:")
    print("  - resultados_objetivo5.csv")
    print("  - convergencia_objetivo5.png")
    print("  - comparacion_ga_vs_trad.png")


if __name__ == "__main__":
    main()