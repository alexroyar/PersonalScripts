#!/usr/bin/env python
# -*- coding: utf-8 -*-


# GESTION DE IMAGENES

# Script que se encarga de detectar archivos duplicados, eliminar estos y dejar
# los archivos restantes con un mismo formato.

# Instalación de programa:
# Tiene que haber una carpeta para las imágenes definitivas
# y otra carpeta para las imágenes nuevas que se quieren
# añadir a la colección.

# Pasos a seguir.
# 1.- Detectar imágenes duplicadas
# 2.- Descartar imágenes duplicadas de carpeta nueva
# 3.- Detectar último nombre del patrón de imágenes definitivas
# 4.- Renombrar imágenes nuevas al patrón definitivo
# 5.- Mover las imágenes nuevas a la carpeta definitivas

import os,shutil,subprocess

#CONFIGURACION:
barra = "/"
carpeta_definitiva = "Correctas"
carpeta_nuevas = "pasar"
nombre_archivo = "file_"
formatos_multimedia=["jpg","jpeg","png","gif","avi","mpg","wmv","rmvb","mkv","3gp","mov","flv","mp4"]

path = os.getcwd()+barra

print "Configuracion:"
print "· Carpeta definitivas:",carpeta_definitiva
print "· Carpeta nuevas:",carpeta_nuevas
print "· Current path:",path

raw_input("\nEnter para buscar duplicados...")

# Colección de imagenes en carpeta definitivas
imagenes_definitivas = [x for x in os.listdir(path+carpeta_definitiva) if x.split(".")[-1] in formatos_multimedia] # linux
# Colección de imágenes en carpeta a pasar
imagenes_nuevas=subprocess.check_output("find pasar/ -type f",shell=True).split("\n")[:-1]
imagenes_nuevas = [x for x in imagenes_nuevas if ".thumbnail" not in x and x.split(".")[-1] in formatos_multimedia]

#imagenes_nuevas = [x for x in os.system("find "+carpeta_nuevas+"/ -type f") if x.split(".")[-1] in formatos_multimedia] # linux
# Siguiente imagen a guardar en carpeta definitivas
if len(imagenes_definitivas)>0:
	siguiente_imagen_definitiva = max([int(x.split("_")[-1].split(".")[0]) for x in imagenes_definitivas])+1
else:
	siguiente_imagen_definitiva = 1

# Recupero imágenes duplicadas
os.system("fdupes -r "+path+"> temp.txt")
f = open("temp.txt","r")
dup_temp = [x.strip() for x in f.readlines()]

duplicadas = []
temp=[]
for x in dup_temp:
	if x != "":
		temp.append(x)
	else:
		if len(temp)>0:duplicadas.append(temp)
		temp=[]
f.close()
###

#Convierto ruta /home/xx/file.yy a /home/xx
quitar_nombre = lambda x:("/").join(x.split("/")[:-1])
solo_nombre = lambda x:x.split("/")[:-1]
def s_nombre(x):
	return x.split("/")[-1]

#Genero una lista para seleccionar las imágenes que se eliminarán de la lista de duplicados
descartar_tmp=[]
for grupo in duplicadas:
	temp=[]
	for archivo in grupo:
		if path+carpeta_definitiva not in archivo: temp.append(archivo)
		else: temp.append("descartar")

	if "descartar" in temp:
		temp.remove("descartar")
		descartar_tmp.append(temp)
	elif len(temp)>1:descartar_tmp.append(temp[:-1])
	else:descartar_tmp.append(temp)

#Genero una lista total de archivos que se tienen que descartar en el volcado
#ya que están repetidas.
descartar=[archivo for grupo in descartar_tmp for archivo in grupo]

#Genero lista con las imágenes que se tienen que copiar ya que son realmente nuevas.

imagenes_nuevas=[path+x for x in imagenes_nuevas]
copiar = [x for x in imagenes_nuevas if x not in descartar]
#Información a continuar:
print "\n\nInformación de volcado:"
print "· Se van a descartar",len(descartar),"imágenes duplicadas de un total de",len(imagenes_nuevas),"."
print "· Finalmente se agregarán",len(copiar),"imágenes a la colección."
raw_input("\nPresiona enter para ver informe de duplicados")
for i in descartar:print i
raw_input("\nPresiona enter para añadir las imágenes a la colección...")

#Agrego imagenes a la carpeta definitiva
for archivo in copiar:
	original = archivo
	final = path+carpeta_definitiva+barra+nombre_archivo+str(siguiente_imagen_definitiva)+"."+archivo.split(".")[-1]
	print "· Copiando:",original,"->",final
	shutil.copy2(original,final)
	siguiente_imagen_definitiva +=1



