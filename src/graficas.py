import matplotlib.pyplot as plt

def graficar_resultados(
    generaciones,
    maximos,
    minimos,
    promedios,
    cant_corridas
):

    plt.figure(figsize=(10, 6))

    plt.plot(generaciones, maximos, label="Máximos")
    plt.plot(generaciones, minimos, label="Mínimos")
    plt.plot(generaciones, promedios, label="Promedios")

    plt.xlabel("Generación")
    plt.ylabel("Valor función objetivo")

    plt.title(f"Algoritmo Genético - {cant_corridas} corridas")


    if cant_corridas == 20:
        plt.xticks(range(0, cant_corridas, 1))

    elif cant_corridas == 100:
        plt.xticks(range(0, cant_corridas, 10))

    elif cant_corridas == 200:
        plt.xticks(range(0, cant_corridas, 20))

    plt.legend()

    plt.grid(True)

    plt.show()