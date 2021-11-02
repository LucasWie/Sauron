from skbio import DNA
from skbio.alignment import local_pairwise_align_ssw, local_pairwise_align

"""Función dedicada a alinear un par de secuencias de ADN y devolver la región con coincidencia."""

def alinear(str1, str2):
    
    str1 = "G" + str1
    str2 = "G" + str2
    cadena1 = DNA(str1)
    cadena2 = DNA(str2)
    resultados = local_pairwise_align_ssw(cadena1, cadena2, gap_open_penalty = 3)
    
    texto = str(resultados)
    
    texto = list(texto.split("\n"))
    #print(texto)
    query = texto[6]
    ultima_linea = texto[7]
    alineado = list(ultima_linea.split(","))[0]
    score = int(list(ultima_linea.split(","))[1])
    pos_ini1 = list(ultima_linea.split(","))[2]
    pos_ini2 = list(ultima_linea.split(","))[4]
    

  
    if (pos_ini1 == " [(0" or pos_ini2 == " (0"):
        query = query[1:len(query)]
        alineado = alineado[1:len(alineado)]
        score = int(score)-2

    return (query,alineado,score)

if __name__ == "__main__":
    uno = "TATTGA"
    dos = "TATGGA"
    print(alinear(uno, dos))
    