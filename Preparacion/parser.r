#Obtener las cepas de firmicutes y su URL de descarga
datos<-read.csv("prokaryotes.csv")
datos<-datos[,c(1,2,8)]
# Hasta acá solamente tengo un DF con los nombres de organismos, cepas
# el URL desde donde descargar su genoma y algunos otros datos

#Ahora para cada Nombre de organismo, debo poder recuperar los URL... de todas las cepas 

#Como algunos organismos incluyen la cepa en su nombre,
#debo quedarme solo con las primeras dos palabras (genero y especie)

colnames(datos)<-c("Organismo","Cepa","FTP")
datos$Organismo<-as.factor(datos$Organismo)
procesar<-datos$Organismo
procesar<-as.character(procesar)

for (i in 1:length(procesar)){
  auxiliar <- strsplit(procesar[i],split=" ")
  auxiliar <- unlist(auxiliar)
  procesar[i] <- paste(auxiliar[1],auxiliar[2])
}

procesar<-as.factor(procesar)
datos$Organismo<-procesar
#y ahora tengo todos los organismos con el mismo nombre y puedo agruparlos.

datos<-datos[order(datos$Organismo),]
fila<-1
bacteria<-as.character(datos$Organismo[1])
while( fila < length(datos$Organismo)){
  print(paste0("Las cepas de ",bacteria," son:"))
  while ((as.character(datos$Organismo[fila])==bacteria) & fila<=length(datos$Organismo)) {
    print(as.character(datos$Cepa[fila]))
    fila<-fila+1
  }
    if(fila<=length(datos$Organismo))  
  bacteria<-datos$Organismo[fila]
}

#
lista<-list()
estructura_vacia<-data.frame("Cepa"=vector(),"URL"=vector() )
for (i in 1:length(levels(datos$Organismo))){lista[[i]]<-estructura_vacia}
names(lista)<-levels(datos$Organismo)

##Nombres para las columnas de cada DF correspondiente a un organismo
fila<-15
bacteria<-as.character(datos$Organismo[15])
print(bacteria)
while( fila <= length(datos$Organismo)) {
  print(paste0("Las cepas de ",bacteria," son:"))
  while ((as.character(datos$Organismo[fila])==bacteria) & fila<=length(datos$Organismo)) {
    lista[[grep(bacteria,names(lista))]] <- rbind(lista[[grep(bacteria,names(lista))]],cbind(("Cepa"=as.character(datos$Cepa[fila])),"URL"=as.character(datos$FTP[fila])))  
    print(lista[[grep(bacteria,names(lista))]])
    fila<-fila+1
  }
  if(fila<=length(datos$Organismo)){
    bacteria<-as.character(datos$Organismo[fila])
    }
  
}

 
# Reescribir con un formato que pueda encontrar todas las cepas oredenadas por organismo y donde
# disponga del url para descargarlo.

system("mkdir enterobacterias_cepas")
path<-as.character(paste(getwd(),"/Datos_Genbank",sep=""))
setwd(path)
genero<-unlist(strsplit(names(lista[1]),split=" "))[1]



for (i in 1:length(lista)){
  if (genero!=unlist(strsplit(names(lista[i]),split=" "))[1]){
    genero<-unlist(strsplit(names(lista[i]),split=" "))[1]
    setwd(path)
    system(paste("mkdir",genero,sep=" "))
    setwd(paste(path,"/",genero,sep=""))
    write.csv(lista[[i]], file=(names(lista)[i]),row.names = FALSE)
  }
  else{
    write.csv(lista[[i]], file=(names(lista)[i]),row.names = FALSE)
  }

}
