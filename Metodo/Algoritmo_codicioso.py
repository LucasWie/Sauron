import os
import networkx as nx
import vntr_tools2 as vt
import copy

"""Contiene las funciones que aplican el algoritmo greedy modificado de set cover . Devuelve un set con los nodos necesarios"""


    #Peso: Es el peso que tiene que una cepa ya se haya incluido o no. busco cubrir mas de una vez todas las cepas, pero al elegir le doy preferencia a las menos elegidas
    #Redundancia: El numero de redundancia deseado es la cantidad maxima de veces que quiero incluir cada cepa en el conjunto
    #max_num_vntrs: El numero maximo de vntrs que estoy dispuesto a devolver como salida
    

def calcular_cobertura(Grafo, cover, cubrir, peso=3, num_redundancia=5, max_num_vntrs=10):
    G = copy.deepcopy(Grafo)
    covering = copy.deepcopy(cover)
    a_cubrir = copy.deepcopy(cubrir)
    grupos = {}
    set_salida = []
    for nodo in covering:
        grupos[nodo] = G[nodo]
    
    
    cepas = list(a_cubrir)
    valor_por_cepa = {}
    for cepa in cepas:
        valor_por_cepa[cepa] = peso * num_redundancia  # Inicialización

    while (len(a_cubrir) > 0 and len(set_salida) < max_num_vntrs and len(grupos) > 0):
        #encontrar el set que cubre mayor cantidad de nodos de "a_cubrir" y guardarlo en el set salida
        nodo_maximo = find_max(grupos,valor_por_cepa)
        if (nodo_maximo == " "):
            break

        set_salida.append(nodo_maximo)
        covering.discard(nodo_maximo)
        #eliminar del grafo todos los nodos ya cubiertos
        for key in (G[nodo_maximo].keys()):
            a_cubrir.discard(key)
            valor_por_cepa[key] = valor_por_cepa[key] - peso
        for cepa in cepas:
            if valor_por_cepa[cepa] == 0:
                a_cubrir.discard(cepa)
                G.remove_node(cepa)
        cepas=list(a_cubrir)
        G.remove_node(nodo_maximo)
        
        #repetir
        grupos = {}
        for nodo in covering:
            grupos[nodo] = G[nodo]

    return set_salida
    

def find_max(diccionario,cantidades):
    max_aux = 0
    key_max = " "
    for key in diccionario.keys():
        suma = 0
        for cepa in diccionario[key].keys():
            suma = suma + cantidades[cepa]
        if suma > max_aux:
            max_aux = len(diccionario[key])
            key_max = key
    return key_max

if __name__ == "__main__":
    G = nx.Graph()
    G.add_edges_from([("A","1"),("A","3"),("B","1"),("B","2"),("C","3"),("D","2"),("A","4")])

    grupos=nx.bipartite.color(G)
    nx.set_node_attributes(G,grupos,"bipartite")
    top = {n for n, d in G.nodes(data=True) if d['bipartite']==0}
    bottom = set(G) - top

    covertura=greedy_set_cover(G,top,bottom,1,1)

    print (covertura)
