# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 17:18:43 2016
    @author: Laura
"""
"""
    * Librerias para abrir imagenes,recorrer Directorios y
    * crear archivos CSV
"""

from PIL import Image  #libreria que importa las imagenes
import matplotlib.image as mpimg #libreria para abrir imagen
import os #libreria para interacturar con el sistema operativo
import csv #libreria para crear el archivo

class Extraccion_de_caract(): #clase
    
    """
        * Crea el dataset con el permiso de escritura
        * Tiene como delimitador ';'
    """
    abrir = open('dataset.csv','a',newline='') #aqui se crea el dataset en un excel
    registro = csv.writer(abrir,delimiter=';') #escribe lo que genera las caracteristicas delimitads con ;
    """
        * Método anaalizarImagen
        * Parametros: ruta de imagen, nombre de clase
        * Retorna: no regresa ningun tipo de dato
        * Funcionamiento:
        *  abre la imagen que se le pasa en los parametros
        *  obtiene el tamaño de la imagen y se obtiene la razon del tamaño
        *  de la imagen, la razon de los 1's en 6 vectores, 
    """
    def analizarImagen(ruta,clase,cont2): #función analizar la imagen donde los parametros son la ruta y la clase
        data = []#se declara arreglo para guardar las caaracteristicas
        img = Image.open(ruta) #Abre imagen
        img2 = mpimg.imread(ruta) #Abre imagen
        columnas, filas = img.size #Se obtienen las filas y columnas
               
        #Se insertan datos en el array data
        data.extend(Extraccion_de_caract.vectoresImg(img2,filas,columnas))#se llama al metodo vectoresImg y se inserta en
        #en el array data el array recibido
        data.extend(Extraccion_de_caract.cortes(img2,filas,columnas))
        data.append(Extraccion_de_caract.razonFC(columnas,filas))#se inserta la razon de la col/fil
        #llamando al metodo razonFC
        data.append(Extraccion_de_caract.razon_1_img(columnas,filas,img2))#inserta en el array data el numero de 1's
        #en la imagen
        data.append(clase)
        data.append(cont2)
        Extraccion_de_caract.registro.writerow(data) #los escribe en el excel

    """
        * Método: razonFC
        * Parametros: Numero de filas y numero de columnas
        * Retorna: la razon de las filas/columnas
        * Funcionamiento:
        *  regresa la division de col/fil
    """
    def razonFC(col, fil): #función llamada razon de fillas y columnas
        #caracteristica 1 razon
        razon= col/fil #saca la razón de columnas entre filas
        return razon #regresa la razón

    """
        * Método razon_1_img
        * Parametros: Imagen iterable, numero de filas, numero de columnas
        * Retorna: la razon de el numero de 1's/filas*columnas
        * Funcionamiento:
        *  Cuenta el numero de 1's en la imagen y lo divide entre el total de la imagen (filas*columnas)
    """
    def razon_1_img(columnas,filas,img2): #funcion que saca los unos que hay en la razón
        #caracteristica 3    1's/tamaño de la imagen(filas*columnas)
        cuenta_1s = 0 #contador que se encarga de "contar" el numero de unos que existen
        for recorre_fila in range(filas): #recorre todas las filas
            for recorre_col in range(columnas): #recorre las columnas
                if(img2[recorre_fila][recorre_col] == 1):#se compara el valor que hay en imagen[recorrefila][recorre_col] == 1
                    cuenta_1s += 1#se incrementa contador de 1s
        razon = cuenta_1s/(filas*columnas)#se divide entre el area de la imagen para saber la razon
        return razon #nos regresa la razón
        
    """
        * Método vectoresImg
        * Parametros: Imagen iterable, numero de filas, numero de columnas
        * Retorna: vector con 6 razones de la imagen, 3 verticales y 3 horizontales
        * Funcionamiento:
        *  Cuenta el numero de 1's en un vector dado de la imagen, 3 verticales y 3 horizontales.
        *  Verticales: mitad de imagen(col/2), cuarto de imagen (col/4) y tres cuartos imagen (3*(col/4))
        *  Horizontales: mitad de imagen(fil/2), cuarto de imagen (fil/4) y tres cuartos imagen (3*(fil/4))
    """
    def vectoresImg(img,fil, col):
        vectores = [0,0,0,0,0,0]#arreglo para guardar los contadores
        #el siguiente for obtiene el numero de 1s verticales de la imagen
        for indice in range(fil):
            if(img[indice][int(col/2)] == 1):#compara el valor de la posicion de la imagen si es == 1
                vectores[0] += 1#se aumenta contador
            if(img[indice][int(col/4)] == 1):#compara el valor de la posicion de la imagen si es == 1
                vectores[1] += 1#se aumenta contador
            if(img[indice] [int(col*3/4)] == 1):#compara el valor de la posicion de la imagen si es == 1
                vectores[2] += 1#se aumenta contador
        #el siguiente for obtiene el numero de 1s horizontales de la imagen
        for indice in range(col):
            if(img[int(fil/2)][indice] == 1):#compara el valor de la posicion de la imagen si es == 1
                vectores[3] += 1#se aumenta contador
            if(img[int(fil/4)][indice] == 1):#compara el valor de la posicion de la imagen si es == 1
                vectores[4] += 1#se aumenta contador
            if(img[int(fil*3/4)][indice] == 1):#compara el valor de la posicion de la imagen si es == 1
                vectores[5] += 1#se aumenta contador
        vec = [0.0,0.0,0.0,0.0,0.0,0.0] #arreglo declarado en float para sacar la razón
        for indice in range(len(vec)):#arreglo que devuelve las razones
            if(indice<3): #compara si es menor a tres
                vec[indice] = vectores[indice]/fil #saca las razón de lo que tiene el arrelgo vectores entre filas 
            else:
                vec[indice] = vectores[indice]/col #saca la razóln de lo que tiene el arrelgo vectores entre columnas
        return vec#regresa el vector con las razones
    
    """
        * Método cortes
        * Parametros: Imagen iterable, numero de filas, numero de columnas
        * Retorna: El numero de cortes de la mitad de la imagen y un cuarto de la imagen
        * verticalmente
        * Funcionamiento:
        *  Recorre la imagen en las columnas (col/2) y (col/4), cuenta los cambios de 1's y 0's
        *  y despues divide los cambios entre 2 para determinar los cortes en ese vector.
    """
    def cortes(img2,fil,col): #funcion llamada cortes que recibe los parametros de imagen, filas y columnas
        cortes = [0,0,0,0,0,0]#se guardan contadores
        div = int(col/2) #div guarda el resultado de columnas entre 2
        div2 = int(col/4) #div2 guarda el valor de columnas  entre 4
        div3 = int(div2*3)#operacion de div2 lo multiplica por 3
        
        for indice in range(fil): #for que se utiliza para  recorrer las filas
            if (indice == 0):
                if(img2[indice][div] == 1):#compara el valor de la posicion img[indice][div] si es == 1
                    cortes[0] += 1#aumenta contador
                if(img2[indice][div2] == 1):#compara el valor de la posicion img[indice][div2] si es == 1
                    cortes[1] += 1#aumenta contador
                if(img2[indice][div3] == 1):#compara el valor de la posicion img[indice][div3] si es == 1
                    cortes[2] += 1#aumenta contador
            if(img2[indice][div] != img2[indice-1][div] and indice != 0 and indice != (fil-1)):#compara el valor de la posicion con la posicion siguiente,
            #cuando indice es diferente de 0 y del ultimo indice
                cortes[0] += 1#aumenta contador
            if(img2[indice][div2] != img2[indice-1][div2] and indice != 0 and indice != (fil-1)):#compara el valor de la posicion con la posicion siguiente,
            #cuando indice es diferente de 0 y del ultimo indice
                cortes[1] += 1#aumenta contador
            if(img2[indice][div3] != img2[indice-1][div3] and indice != 0 and indice != (fil-1)):#compara el valor de la posicion con la posicion siguiente,
            #cuando indice es diferente de 0 y del ultimo indice
                cortes[2] += 1#aumenta contador
            if(indice == fil-1):
                if(img2[indice][div] == 1):#compara el valor de la posicion img[x][div] si es == 1
                    cortes[0] += 1#aumenta contador
                if(img2[indice][div2] == 1):#compara el valor de la posicion img[x][div] si es == 1
                    cortes[1] += 1#aumenta contador
                if(img2[indice][div3] == 1):#compara el valor de la posicion img[x][div] si es == 1
                    cortes[2] += 1#aumenta contador
        div = int(fil/2) #div guarda el resultado de columnas entre 2
        div2 = int(fil/4) #div2 guarda el valor de columnas  entre 4
        div3 = int(div2*3)#operacion de div2 lo multiplica por 3
        for indice in range(col): #for que se utiliza para recorrer las columnas
            if (indice == 0): #el indice comienza en 0
                if(img2[div][indice] == 1): #compara el valor de la posicion img[indice][div] si es == 1
                    cortes[3] += 1 #incrementa el contador
                if(img2[div2][indice] == 1): #compara el valor de la posicion img[indice][div2] si es == 1
                    cortes[4] += 1 #incrementa el contador
                if(img2[div3][indice] == 1): #compara el valor de la posicion img[indice][div2] si es == 1
                    cortes[5] += 1 #incrementa el contador
            if(img2[div][indice] != img2[div][indice-1] and indice != 0 and indice != (col-1)): #compara el valor de la posicion con la posicion siguiente,
            #cuando indice es diferente de 0 y del ultimo indice
                cortes[3] += 1 #aumenta el contador 
            if(img2[div2][indice] != img2[div2][indice-1] and indice != 0 and indice != (col-1)): #compara el valor de la posicion con la posicion siguiente,
            #cuando indice es diferente de 0 y del ultimo indice
                cortes[4] += 1 #aumenta el contador
            if(img2[div3][indice] != img2[div3][indice-1] and indice != 0 and indice != (col-1)): #compara el valor de la posicion con la posicion siguiente,
            #cuando indice es diferente de 0 y del ultimo indice
                cortes[5] += 1 #aumenta el contador
            if(indice == col-1):
                if(img2[div][indice] == 1): #compara el valor de la posicion img[x][div] si es == 1
                    cortes[3] += 1 #aumenta el contador
                if(img2[div2][indice] == 1): #compara el valor de la posicion img[x][div] si es == 1
                    cortes[4] += 1 #aumenta el contador
                if(img2[div3][indice] == 1): #compara el valor de la posicion img[x][div] si es == 1
                    cortes[5] += 1
        return cortes #regresa cortes
    
    """
        * Método main
        * Parametros: NoAplica
        * Retorna: NoAplica
        * Funcionamiento:
        *  Inicia el programa, Controla el recorrido de las carpetas y los archivos,
        *  envia al metodo 'analizarImagen' la ruta y clase de la imagen a analizar.
        *  Se tiene un if con el archivo 'Thumbs.db' ya que no es procesable por el
        *  programa y este tipo de archivo se crea automaticamente por Windows
    """
    def main(self): #función main
        cont2 =1#numero de instancias es el contador que lleva en que numero está de las lineas
        cont = 0 #contador para las carpetas
        for dirName, subdirList, fileList in os.walk('C:/Users/Laura/Desktop/ocrD/imagenes'):#hace el recorrido de directorio y de archivos      
            if(cont > 0):
                print("    Extrayendo características ..... "+str(dirName[len(dirName)-1]))#impresion de la caracteristica procesada
                for fname in fileList:  #manda a generar las caracteristicas
                    if(fname != 'Thumbs.db'): #esta condición es por que windows genera este tipo de archivos
                        Extraccion_de_caract.analizarImagen((dirName + '/' + fname),(dirName[len(dirName)-1]),cont2)#se pasa el archivo al metodo obtener caracteristicas
                        #print(dirName)
                        cont2  += 1#contador para saber el numero de instancia
            cont += 1 #incrementa contador
        Extraccion_de_caract.abrir.close()#se cierra el archivo CSV

    def __init__(self): #contructor de la calsse
        pass
    