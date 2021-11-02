import TR_tools
from complementar_invertir import * 

"""Este paquete tiene las funciones necesarias para guardar los datos de los vntr"""


def guardar_vntrs_y_reps (G, cepas, vntrs, nombre_salida):
    with open (nombre_salida, "wt") as salida:
        header=[]
        header.append("Nombre de la cepa")
        header.append("Genero")
        cepas = list(cepas)
        vntrs = list(vntrs)
        for vntr in vntrs:
            header.append(vntr)
        salida.writelines(",".join(header))
        salida.write("\n")
        for cepa in cepas:
            #separar nombre de la cepa
            nombre_solo_cepa = list(cepa.split("._."))[0]
            genero = str(list(cepa.split("._."))[1]) + "-" + str(list(cepa.split("._."))[2])
            lista_vntrs = []
            lista_vntrs.append(nombre_solo_cepa)
            lista_vntrs.append(genero)
            for vntr in vntrs:
                if cepa in G[vntr]:
                    lista_vntrs.append(str(int(round(G[cepa][vntr]['weight']))))
                else:
                    lista_vntrs.append("0")
            
            salida.writelines(",".join(lista_vntrs))   
            salida.write("\n")


def guardar_vntrs_y_cebadores (lista_locis,path):
    """Guarda para todos los vntrs recibidos en una lista su id y sus regiones flanqueantes"""
    with open (path,"wt") as salida:
        salida.write("Id,Upstream,Patron,Downstream,Genoma,Inicio,Fin,Porcentaje_GC_total,\n")
        for loci in lista_locis:
            linea_a_escribir = ""
            patron = loci.patron
            genoma = str(loci.nombre_secuencia)
            porcentaje_GC_total = porcentaje_GC(loci.upstream_50 + loci.downstream_50)
            linea_a_escribir = str(loci.id) + "," + loci.upstream_50 + "," + patron + "," + loci.downstream_50 + "," + genoma + "," + str(loci.pos_ini) + "," + str(loci.pos_fin) + "," + str(round(porcentaje_GC_total,2))
            salida.write(linea_a_escribir)
            salida.write("\n")
    
    return True

if __name__ == "__main__":
    pass