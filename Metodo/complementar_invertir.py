"""Par de funciones para obtener los primers de los vntrs una vez elegidos"""

def complementar_secuencia(secuencia):
    secuencia=list(secuencia)
    secuencia_inversa=[]
    for base in range(len(secuencia)):
        if secuencia[base]=="A":
            secuencia_inversa.append("T")
        if secuencia[base]=="C":
            secuencia_inversa.append("G")
        if secuencia[base]=="G":
            secuencia_inversa.append("C")
        if secuencia[base]=="T":
            secuencia_inversa.append("A")
    return "".join(secuencia_inversa)

def invertir_seq(secuencia):
    #complemento=complementar_secuencia(secuencia)
    complemento=list(secuencia)
    invertida=[]
    largo=len(complemento)
    for i in range(largo-1,-1,-1):
        invertida.append(complemento[i])
    invertida="".join(invertida)
    return invertida

def complementar_invertir(secuencia):
    comp_inv=(invertir_seq(complementar_secuencia(secuencia)))
    return (comp_inv)

def porcentaje_GC(secuencia):
    secuencia = secuencia.upper()
    G = secuencia.count("G")
    C = secuencia.count("C")
    GC = G + C
    porcentaje_GC = (GC/len(secuencia))*100
    return(porcentaje_GC)

if __name__ == "__main__":
    upstream=["GATGG","GTCGAGC","GATAGAACCA"]
    print(upstream)
    print(list(map(complementar_secuencia,upstream)))
    print(list(map(complementar_invertir,upstream)))
