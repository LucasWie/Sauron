import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import sys

import TR_tools as vt #Lector lee datos que estan en la salida de TRF407b y funciones para manejar vntr  
from Algoritmo_codicioso import calcular_cobertura #Recibe el bigrafo y aplica el algoritmo codicioso modificado
from Saver import guardar_vntrs_y_reps, guardar_vntrs_y_cebadores  
from Organizador import preparar_entrada 
from Interfaz import pedir_genero_especie 
 
"""Núcleo del sistema. Llama a las funciones necesarias para elegir y cargar datos, organizarlos, evaluarlos y guardarlos"""

#region Permite ejecutar el sistema por consola enviando los parámetros. Si no se envían, los tiene por defecto.
lista_argumentos = sys.argv
if len(lista_argumentos) == 1:   #si no se pasan parametros, usa por defecto
    min_num_variaciones = 2
    paso = 3.0
    num_redundancia = 5
    maximo_permitido = 12
else:
    if len(lista_argumentos) == 5:
        min_num_variaciones = int(lista_argumentos[1])
        paso = float(lista_argumentos[2])
        num_redundancia = int(lista_argumentos[3])
        maximo_permitido = int(lista_argumentos[4])
    else:
        sys.exit("No se pasaron los argumentos correctamente, debe ser: \n1:Mínimo num de variaciones por vntr\n2:Importancia de tener redundancia\n3:Número maximo de redundancia deseado\n4:Máximo numero de loci que se desean encontrar")
#endregion

#region Preparacion
generos_y_especies  = pedir_genero_especie()   #llama a la interfaz
directorio = preparar_entrada(generos_y_especies) #prepara los datos
os.chdir(directorio)  
#endregion

#region Cargar los TR en memoria como objetos TR. 
nombres = os.popen("ls --ignore=*.py --ignore=__*__").read()## Esto guarda en nombres la lista de archivos, que en este caso lon los nombres de los archivos donde se guardan las regiones repeptitivas
nombres = nombres.split(sep = "\n")
nombres = nombres[0:len(nombres)-1] #el último está siempre vacío
super_datos = []
for cepa in nombres:
    super_datos.append(vt.cargar_tr(cepa))
#endregion

#region comparar todos las secuencias en tandem de cada cepa cotra todas las de las demas cepas. 
Grafo = nx.Graph()
Grafo.add_nodes_from(nombres)

contador = 0
for cepa in range(len(super_datos)):
    for secuencia in super_datos[cepa].keys():
        for vntr in super_datos[cepa][secuencia]:
            if(vntr.id == ' '):
                contador += 1
                id_actual = "VNTR_"+str(format(contador,'04d'))
                vntr.id=id_actual
                            
            for cepa2 in range(cepa+1, len(super_datos)):
                for secuencia2 in super_datos[cepa2].keys():
                    for vntr2 in super_datos[cepa2][secuencia2]:
                        if (vntr == vntr2): #aqui entran solo los vntr que comparten patron
                            vntr2.id = id_actual
                            nombre_nodo_a = id_actual 
                            nombre_nodo_b = id_actual 
                            Grafo.add_edge(nombres[cepa], nombre_nodo_a, weight = int(vntr.n_reps))
                            Grafo.add_edge(nombres[cepa2], nombre_nodo_b, weight = int(vntr2.n_reps))
#endregion                            

#region Preparacion visual del grafo
grupos=nx.bipartite.color(Grafo)
nx.set_node_attributes(Grafo,grupos,"bipartite")
top = {n for n, d in Grafo.nodes(data=True) if d['bipartite'] == 0}
bottom = set(Grafo) - top
color_map = []
for node in Grafo:
    if node in top:
        color_map.append("r")
    else:
        color_map.append("b")
posiciones = nx.bipartite_layout(Grafo, bottom)
plt.figure("Inicial")
nx.draw_networkx(Grafo, posiciones, node_color = color_map, with_labels = False, node_size=5)
plt.show()
#endregion

#region Filtrar: solo continuan siendo evaluados los VNTR con mas de "Mínima variabilidad" alelos diferentes
vntrs_no_variables = []
posibles_nreps_por_loci = {}
for llegada in top:
    posibles_nreps_por_loci[llegada] = []
for (salida, llegada, w) in Grafo.edges.data('weight', default = 0):
    if w not in posibles_nreps_por_loci[llegada]:
        posibles_nreps_por_loci[llegada].append(w)
for marcador_posible in top:
    if(len(posibles_nreps_por_loci[marcador_posible]) < min_num_variaciones):
        vntrs_no_variables.append(marcador_posible)
Grafo.remove_nodes_from(vntrs_no_variables)
#endregion

#region Re-ordenamiento del grafo post-filrado
grupos = nx.bipartite.color(Grafo)
nx.set_node_attributes(Grafo,grupos,"bipartite")
top = {n for n, d in Grafo.nodes(data = True) if d['bipartite'] == 0}
bottom2 = set(Grafo) - top
#posiciones = nx.bipartite_layout(Grafo,bottom2)
#plt.figure("Sin no variables")
#nx.draw_networkx(Grafo, posiciones, node_color = color_map, with_labels = False, node_size = 5)
#plt.show()
#endregion

#Finalmente paso los datos para la busqueda usando el algoritmo codicioso
VNTRs_necesarios = calcular_cobertura(Grafo, top, bottom2, paso, num_redundancia, maximo_permitido)
print(VNTRs_necesarios)

#region Re-ordenamiento del grafo. Limpieza de nodos
for loci in top:
    if loci not in VNTRs_necesarios:
        Grafo.remove_node(loci)
# Por prolijidad, para deshacerme de las cepas a las que no se le encontró ningun vntr. 
lista_sin_vntr = []
for grado in Grafo.degree:
    if grado[1] == 0:
        lista_sin_vntr.append(grado[0])
#Borrar los las cepas que no están unidas a nungún VNTR, aquellas inclasificables por el sistema
Grafo.remove_nodes_from(lista_sin_vntr)
grupos = nx.bipartite.color(Grafo)
nx.set_node_attributes(Grafo,grupos,"bipartite")
top = {n for n, d in Grafo.nodes(data=True) if d['bipartite'] == 0}
bottom3 = set(Grafo) - top
#coloreo de los nodos, solo visual
color_map = []
for node in Grafo:
    if node in top:
        color_map.append("r")
    else:
        color_map.append("b")

posiciones = nx.bipartite_layout(Grafo,bottom3)
plt.figure("Filtrado final")
nx.draw_networkx(Grafo, posiciones, node_color = color_map, with_labels = False, node_size = 5)
plt.show()
#endregion

#region Escritura de la matriz de los datos. 
path_carpeta_salida="./Resultados/"
combinacion_param=str(min_num_variaciones) + "_" + str(paso) + "_" + str(num_redundancia) + "_" + str(maximo_permitido)
nombre_salida = "output_" + combinacion_param + ".csv"
path_salida = path_carpeta_salida + nombre_salida
guardar_vntrs_y_reps(Grafo, bottom, top, path_salida)

lista_final = []
for cepa in range(len(super_datos)):
    for secuencia in super_datos[cepa].keys():
        for vntr in super_datos[cepa][secuencia]:
            if vntr.id in VNTRs_necesarios and (vntr not in lista_final):
                lista_final.append(vntr)
nombre_datos_marcadores = "vntr_loci" + combinacion_param + ".csv"
if guardar_vntrs_y_cebadores(lista_final, path_carpeta_salida+nombre_datos_marcadores):
    print("Se guardaron los vntrs y sus primers para su uso o estudio posterior")
#endregion

##Eliminar el directorio auxiliar creado cuando se llamo "preparar_entrada"
os.chdir("./Datos_Preprocesados")
os.system("rm -r " + directorio)
