import distance as d
from alineamiento import alinear

"""Definicion de la clase TR. Incluye todos los datos brindados por TRF y métodos necesarios (igualdad de TR y carga desde archivos)"""

class TR:
    def __init__(self,lista_datos):
        self.__id_vntr__ = ' '
        self.__pos_ini__ = int(lista_datos[0])
        self.__pos_fin__ = int(lista_datos[1])
        self.__largo_patron__ = float(lista_datos[2])
        self.__num_repeticiones__ = float(lista_datos[3])
        self.__largo_consenso__ = int(lista_datos[4])
        self.__porcen_match__ = lista_datos[5]
        self.__porcen_indel__ = lista_datos[6]
        self.__score__ = lista_datos[7]
        self.__PA__ = lista_datos[8]
        self.__PC__ = lista_datos[9]
        self.__PG__ = lista_datos[10]
        self.__PT__ = lista_datos[11]
        self.__entropy__ = lista_datos[12]
        self.__patron_consenso__ = lista_datos[13]
        self.__secuencia__ = lista_datos[14]
        self.__region_upstream__ = lista_datos[15]
        self.__region_downstream__ = lista_datos[16]
        self.__secuencia_origen__ = lista_datos[17]
        self.__secuencia_origen__ = self.__secuencia_origen__.split(",")[0]
        self.__secuencia_origen__ = self.__secuencia_origen__.split(" ")[1:len(self.__secuencia_origen__.split(" "))]
        self.__secuencia_origen__ = " ".join(self.__secuencia_origen__)

    @property
    def id(self):
        return self.__id_vntr__
    
    @id.setter
    def id(self,nuevoid):
        self.__id_vntr__ = nuevoid

    @property
    def n_reps(self):
        return self.__num_repeticiones__
    
    @property
    def largo_patron(self):
        return self.__largo_patron__

    @property
    def patron(self):
        return self.__patron_consenso__
    
    @property
    def upstream_50(self):
        return self.__region_upstream__

    @property
    def downstream_50(self):
        return self.__region_downstream__   

    @property
    def pos_ini(self):
        return self.__pos_ini__ 

    @property
    def pos_fin(self):
        return self.__pos_fin__ 

    @property
    def nombre_secuencia(self):
        return self.__secuencia_origen__


    def __str__(self):
        salida = "TR" + str(self.id) + " patron: " + self.patron #+" y "+str(self.n_reps)+" repeticones."  
        return(salida)

## Igualdad de vntrs compara dos vntr por su patron y su secuencia flanqueante:

    def is_same_vntr(self, tr2, tolerancia_patron=5, tolerancia_flanq=5):
        son_iguales = False
         
        if (len(self.upstream_50) == len(tr2.upstream_50)) and (len(self.downstream_50) == len(tr2.downstream_50)):
            if((d.hamming(self.upstream_50,tr2.upstream_50)/50)*100 < tolerancia_flanq) and ((d.hamming(self.downstream_50 , tr2.downstream_50)/50)*100 < tolerancia_flanq):
                if (abs(len(self.patron)-len(tr2.patron)) < 0.1*len(self.patron)):#dos patrones seran considerados para evaluar como iguales solo su diferencia de longitud es menor a un 10%
                    if( (len(alinear(self.patron,tr2.patron)[1])/int(self.largo_patron))*100 > (100 - tolerancia_patron) ): #patron
                        son_iguales=True

  
        return son_iguales   

    def __eq__(self,otro_tr):
        igualdad=False
        #if (self.id != " "):
        
        if (self.id==otro_tr.id):
            igualdad=True
        else:
            if self.is_same_vntr(otro_tr):
                igualdad=True
        return igualdad    

def cargar_tr(nombre_cepa):
    with open (nombre_cepa,"rt") as archivo:
        datos=archivo.readlines()
        secuencias_de_cepa=[]
        TR_seq={}
        
        for line in datos:
            if line[0] == "@":#busca "secuencia" porque solo dspues de es palabra estan los datos utiles.  
                nombre_secuencia = line[1:len(line)-1] #guarda el nombre
                nombre_secuencia = nombre_secuencia.rstrip()
                secuencias_de_cepa.append(nombre_secuencia)
                TR_seq[nombre_secuencia] = []  
            else:
                datos_tr = line.split(" ")
                for i in range(len(datos_tr)):
                    datos_tr[i] = datos_tr[i].strip()   
                datos_tr.append(nombre_secuencia)
                tr_aux = TR(datos_tr)                      
                TR_seq[nombre_secuencia].append(tr_aux)
    return(TR_seq)


   # print (cepa)
