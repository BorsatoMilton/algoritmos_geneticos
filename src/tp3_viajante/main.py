import pandas as pd
from metodos_de_busqueda import ingresar_provincia, sin_ingresar_provincia, resolver_por_ag

def main():
    df = pd.read_excel("TablaCapitales.xlsx", index_col=0)
    df = df.iloc[:24, :24]
    df.columns = df.index

    lista_filas = df.index.tolist()

    while True:
        print("\nMENU")
        print("1. Ingresar Provincia")
        print("2. Recorrido Mínimo")
        print("3. Resolver por AG")
        print("4. Salir")

        try:
            decision = int(input("Ingrese una opción: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue

        if decision < 1 or decision > 4:
            print("Opción inválida. Intente nuevamente.")
            continue

        if decision == 1:
            ingresar_provincia(lista_filas, df)
        elif decision == 2:
            sin_ingresar_provincia(lista_filas, df)
        elif decision == 3:
            resolver_por_ag(lista_filas, df)
        elif decision == 4:
            print("Saliendo del programa...")
            break 


if __name__ == "__main__":
    main()