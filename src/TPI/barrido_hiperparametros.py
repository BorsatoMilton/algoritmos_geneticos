import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ga import ejecutar_optimizacion
from funciones import calcular_energia_anual
from config import cargar_datos_clima, ANGULOS_TRADICIONALES, PERDIDAS_SISTEMA, POTENCIA_PICO_KWP

# Configuraciones a comparar: (pop_size, n_generaciones)
CONFIGURACIONES = [
    (20, 10),
    (20, 30),
    (50, 20),
    (100, 30),  
]
REPETICIONES_POR_CONFIG = 5  # corridas por config
carpeta_resultados = "graficos"
os.makedirs(carpeta_resultados, exist_ok=True)


def main():
    print("Descargando/generando TMY...")
    datos_clima, sol, dni_extra, airmass = cargar_datos_clima()

    energia_tradicional = calcular_energia_anual(
        ANGULOS_TRADICIONALES, datos_clima, sol, dni_extra, airmass,
        PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
    )

    filas = []

    for pop_size, n_gen in CONFIGURACIONES:
        print(f"\n=== Config: pop_size={pop_size}, n_generaciones={n_gen} ===")
        energias = []
        tiempos = []

        for rep in range(REPETICIONES_POR_CONFIG):
            mejor_individuo, historial, tiempo = ejecutar_optimizacion(
                datos_clima, sol, dni_extra, airmass,
                pop_size=pop_size, n_generaciones=n_gen,
                perdidas_sistema=PERDIDAS_SISTEMA, potencia_pico_kwp=POTENCIA_PICO_KWP,
                seed=rep, verbose=False
            )
            energia = calcular_energia_anual(
                mejor_individuo, datos_clima, sol, dni_extra, airmass,
                PERDIDAS_SISTEMA, POTENCIA_PICO_KWP
            )
            energias.append(energia)
            tiempos.append(tiempo)
            print(f"  rep {rep}: energía={energia:.2f} kWh, tiempo={tiempo:.2f}s")

        energias = np.array(energias)
        tiempos = np.array(tiempos)
        mejora_pct = ((energias.mean() - energia_tradicional) / energia_tradicional) * 100

        filas.append({
            "pop_size": pop_size,
            "n_generaciones": n_gen,
            "evaluaciones_totales": pop_size * n_gen,
            "energia_media_kwh": energias.mean(),
            "energia_std_kwh": energias.std(),
            "mejora_pct_vs_tradicional": mejora_pct,
            "tiempo_medio_seg": tiempos.mean(),
            "tiempo_std_seg": tiempos.std(),
        })

    df = pd.DataFrame(filas)
    ruta_csv = os.path.join(carpeta_resultados, "barrido_hiperparametros.csv")
    df.to_csv(ruta_csv, index=False)
    print("\n=== TABLA RESUMEN ===")
    print(df.to_string(index=False))

    # Grafico: tiempo contra calidad, tamaño de punto = precisión (menor std = más chico)
    plt.figure(figsize=(7, 5))
    for _, row in df.iterrows():
        plt.scatter(row["tiempo_medio_seg"], row["energia_media_kwh"],
                    s=150, label=f"pop={row['pop_size']}, gen={row['n_generaciones']}")
        plt.errorbar(row["tiempo_medio_seg"], row["energia_media_kwh"],
                     yerr=row["energia_std_kwh"], fmt="none", ecolor="gray", capsize=4)
    plt.axhline(energia_tradicional, color="red", linestyle="--", label="Tradicional")
    plt.xlabel("Tiempo medio por corrida (s)")
    plt.ylabel("Energía media obtenida (kWh)")
    plt.title("Trade-off: tiempo de cómputo vs. calidad de solución")
    plt.legend(fontsize=8)
    plt.tight_layout()
    ruta_archivo = os.path.join(carpeta_resultados, "grafico_tiempo_vs_calidad.png")
    plt.savefig(ruta_archivo, dpi=150)
    plt.close()

    print("\nArchivos generados: barrido_hiperparametros.csv, grafico_tiempo_vs_calidad.png")


if __name__ == "__main__":
    main()