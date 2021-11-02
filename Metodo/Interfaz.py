"""Este script se encarga de interactuar con el usuario, en la parte de elegir las cepas de entrada.""" 

def pedir_genero_especie():
    generos_entrada={}
    validos=["Escherichia","Yersinia","Shigella","Klebsiella","Morganella","Providencia","Cronobacter","Salmonella","Fin","0"]
    aux_in=input("Ingrese un genero:\n")
    #print(aux_in)   
    while (not(aux_in == "Fin")):
        #print("pinche pendejo")
        while (not (aux_in.lower().capitalize() in validos)):
            print("Ese género no es válido")
            #print(f"Los generos ingresados hasta ahora son: \n",generos_entrada)
            aux_in = input("Ingrese un genero, Fin para salir\n")
        if (not(aux_in == "0" or aux_in == "Fin")):
            genero_actual = aux_in.lower().capitalize()               
            generos_entrada[genero_actual]=list()
            print(f"El genero ingresado fue: ",genero_actual)
            aux_in = input("Ingrese una especie, 0 para continuar\n")
            while(not(aux_in == "0" or aux_in == "Fin")):
                generos_entrada[genero_actual].append(aux_in)
                aux_in = input("Ingrese una especie, 0 para continuar\n")
        aux_in = input("Ingrese un genero, Fin para salir\n")
    return generos_entrada


if __name__ == "__main__":
    dic = pedir_genero_especie()
    print(dic)