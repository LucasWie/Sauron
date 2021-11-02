import csv
from os import system

"""Usando los datos de 'Datos_Genbank' organiza, descarga y pre-procesa genomas"""

def descargar_y_buscar(path):
        #Parámetros para enviarle a TRF
        match = 2; mismatch = 7; indel = 30; pm = 80; pi = 10; minscore = 50; maxpatern = 300
        parametros_trf_lista = [str(match),str(mismatch),str(indel),str(pm),str(pi),str(minscore),str(maxpatern)]
        parametros_trf = " " + ' '.join(parametros_trf_lista)
        opciones_trf = " -h -d -ngs" #quiero un único archivo, completo para todo y con regiones flanqueeantes
        especie = path.split(sep="/")[len(path.split(sep="/"))-1]
        especie = especie.split(sep=" ")[0] + "_" + especie.split(sep=" ")[1]
        path_salida = "./Datos_Preprocesados/" + especie + "_VNTRs"
        system("mkdir " + path_salida)
        
        with open (path) as archivo:
                cepas = csv.reader(archivo,delimiter=',')
                next(cepas) # esto saltea el encabezado para no descargar el titulo
                for cepa in cepas:
                        print(cepa[0] + " se descarga desde:")
                        print(cepa[1])
                #Aca le agrego "_genomic.fna.gz" para que descargue unicamente la secuencia pero no los metadatos
                        lista_aux = cepa[1].split("/")    
                        nombre_archi = lista_aux[len(lista_aux)-1]   
                        extension = '_genomic.fna.gz'
                        nombre_secuencia = nombre_archi+extension
                        ftp_final = cepa[1] + '/' + nombre_secuencia
                
                # Descarga 
                        system("wget " + ftp_final + " -q --progress=bar:force:noscroll --show-progress")#para que wget sea mas amigable
                        system("gzip -d " + nombre_secuencia)
                        nombre_secuencia = nombre_secuencia[0:(len(nombre_secuencia)-3)]
                        system("./trf407b " + nombre_secuencia + parametros_trf + opciones_trf + " > " +path_salida + "/'" + cepa[0]+"'")
                        system("rm " + nombre_secuencia)
        return path_salida

if __name__ == "__main__":
    descargar_y_buscar("./Datos_Genbank/Shigella/Shigella boydii") ## Se cambia manualmente para cada especie que se quiera
    
