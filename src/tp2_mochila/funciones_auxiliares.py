def pasar_a_binario(n, cantidad_bits=10):
    binario = []
    while n > 0:
        binario.append(n % 2)
        n //= 2
    
    while len(binario) < cantidad_bits:
        binario.append(0)
        
    binario.reverse()
    return binario