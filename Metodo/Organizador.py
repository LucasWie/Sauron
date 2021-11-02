import os
import shutil
import subprocess
"""Este script se encarga de organizar en una única carpeta todos los archivos con las TR encontradas por TRF para las especies que definió el usuario"""

def preparar_entrada(generos):
    path="./Datos_Preprocesados"
    os.chdir(path)
    destino = "Temporal"
    os.system("rm -rf " + destino)
    os.makedirs(destino)
    for genero in generos.keys():
        for especie in generos[genero]:
                nombre_carpeta = genero + "_" + especie + "_VNTRs"
                archivos=os.listdir(nombre_carpeta)
                for archivo in archivos:
                    shutil.copy2(nombre_carpeta + "/" + archivo, destino + "/" + archivo + "._." + genero + "._." + especie)
    return(destino)
                           

if __name__ == "__main__":
    generos={"Shigella":["flexneri", "dysenteriae"],"Yersinia":["pestis"]}
    preparar_entrada(generos)

