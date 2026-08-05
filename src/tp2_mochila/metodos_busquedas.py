from funciones_auxiliares import pasar_a_binario

def busqueda_exhaustiva(objetos, limite_maximo, metrica):
    valor_maximo = 0
    volumen_maximo = 0
    mejor_combinacion = []


    objetos.reverse()

    cant_objetos = len(objetos)

    for i in range(2**cant_objetos):
        vol_actual = 0
        valor_actual = 0
        
        binario = pasar_a_binario(i, cant_objetos)
        for j in range(len(binario)):
            if binario[j] == 1:
                vol_actual += objetos[j][metrica]
                valor_actual += objetos[j]["valor"]
                
        if vol_actual <= limite_maximo and valor_actual > valor_maximo:
            valor_maximo = valor_actual
            volumen_maximo = vol_actual
            mejor_combinacion = binario

    print("Resultados de la búsqueda exhaustiva:")

    print(f"Valor máximo: {valor_maximo}")
    print(f"Volumen máximo: {volumen_maximo}")
    print(f"Mejor combinación (binario): {mejor_combinacion}")
    print("Mejor combinación:")
    for i in range(len(mejor_combinacion)):
        if mejor_combinacion[i] == 1:
            print(f"Objeto {objetos[i]['id']} seleccionado: {metrica} = {objetos[i][metrica]}, Valor = {objetos[i]['valor']}")


def busqueda_greedy(objetos, limite_maximo, metrica):
    proporciones = []
    valor_actual = 0
    volumen_actual = 0
    combinacion_indices = []

    for i in range(len(objetos)):
        proporcion = objetos[i]["valor"] / objetos[i][metrica]
        proporciones.append((i, proporcion))

    proporciones.sort(key=lambda x: x[1], reverse=True)

    for i in range(len(proporciones)):
        idx_original = proporciones[i][0]
        if volumen_actual + objetos[idx_original][metrica] <= limite_maximo:
            volumen_actual += objetos[idx_original][metrica]
            valor_actual += objetos[idx_original]["valor"]
            combinacion_indices.append(idx_original)        

    print("----------------------------------------------------")
    print("Resultados de la búsqueda greedy:")
    print(f"Valor máximo: {valor_actual}")
    print(f"Volumen máximo: {volumen_actual}")
    print("Mejor combinación:")

    combinacion_indices.sort()
    for idx in combinacion_indices:
        obj = objetos[idx]
        print(f"Objeto {obj['id']} seleccionado: {metrica} = {obj[metrica]}, Valor = {obj['valor']}")