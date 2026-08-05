from metodos_busquedas import busqueda_exhaustiva, busqueda_greedy

def main():
    vol_max = 4200
    peso_max = 3000

    objetos_volumen = [
        {"id": 1,  "volumen": 150,  "valor": 20},
        {"id": 2,  "volumen": 325,  "valor": 40},
        {"id": 3,  "volumen": 600,  "valor": 50},
        {"id": 4,  "volumen": 805,  "valor": 36},
        {"id": 5,  "volumen": 430,  "valor": 25},
        {"id": 6,  "volumen": 1200, "valor": 64},
        {"id": 7,  "volumen": 770,  "valor": 54},
        {"id": 8,  "volumen": 60,   "valor": 18},
        {"id": 9,  "volumen": 930,  "valor": 46},
        {"id": 10, "volumen": 353,  "valor": 28},
    ]

    objetos_peso = [
        {"id": 1,  "peso": 1800,  "valor": 72},
        {"id": 2,  "peso": 600,  "valor": 36},
        {"id": 3,  "peso": 1200,  "valor": 60},
    ]

    decision = input("Seleccione el tipo de búsqueda (1 para volumen, 2 pesos): ")

    while decision not in ["1", "2"]:
        print("Opción no válida. Por favor, seleccione 1 o 2.")
        decision = input("Seleccione el tipo de búsqueda (1 para volumen, 2 pesos): ")

    metrica = "volumen" if decision == "1" else "peso"

    if decision == "1":
        busqueda_exhaustiva(objetos_volumen, vol_max, metrica)
        busqueda_greedy(objetos_volumen, vol_max, metrica)
    else:
        busqueda_exhaustiva(objetos_peso, peso_max, metrica)
        busqueda_greedy(objetos_peso, peso_max, metrica)


if __name__ == "__main__":
    main()