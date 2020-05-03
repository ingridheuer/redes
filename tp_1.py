#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:38:38 2020

@author: ingrid
"""
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from scipy import stats

def abrir(nombre_archivo):
    """Función que nos pasaron en la práctica. Abre los txt y los ordena por columnas"""
    archivo = open(nombre_archivo)
    data=[]
    for linea in archivo:
        linea=linea.strip()
        columna=linea.split()
        data.append(columna)
    return data
 #%%
path = r'/home/ingrid/Documents/redes/tp1/'

files_gml = {'science':'netscience.gml', 'internet':'as-22july06.gml'}
files_txt = {'yeast1':'yeast_Y2H.txt', 'yeast2':'yeast_AP-MS.txt'}

grafos = {}
enlaces = {}

for file in files_gml:
    grafos[file] = nx.read_gml(path + files_gml[file])

for file in files_txt:
    archivo = abrir(path + files_txt[file])
    enlaces[file] = nx.Graph()
    enlaces[file].add_edges_from(archivo)

"sacar nodos sueltos con remove isolates"
#%%
edges = grafos['internet'].edges()

#diccionario con key=nodo, value=grado del nodo
grado_propio = dict(grafos['internet'].degree(weight='value')) 

#idem pero value=grado medio de sus vecinos
grados_vecinos = nx.average_neighbor_degree(grafos['internet'],weight='value')

#Voy a armar un diccionario de nodos agrupados por grado. Las keys van a ser grados, los values listas de nodos.
# Cada vez que el loop pasa por un valor que no está, defaultdict crea la entrada con una lista vacía y le appendea la clave a la lista. 
# Cuando vuelve a pasar por ese valor simplemente appendea la clave a la lista.
d_asort = defaultdict(list) 
for k, v in grado_propio.items():
    d_asort[v].append(k) 

#Similar al anterior. Ahora las key son grados y los values el grado medio de los vecinos de cada nodo del conjunto
d_grados_vecinos = defaultdict(list) 
for k,v in grados_vecinos.items():
    d_grados_vecinos[grado_propio[k]].append(v)

#En base a d_grados_vecinos, armo un diccionario con key=grados, pero ahora tomo el promedio de todos los valores por cada grado.
d_knn = {k: np.mean(v) for k,v in d_grados_vecinos.items()}
#%%
#ploteo knn(k)
plt.scatter(d_knn.keys(),d_knn.values(), color = 'r') 
plt.show()
#%%
#Ordeno los datos para un histograma de distribución de grado. Uso len(n) para contar cuantos nodos hay por cada grado
dist_grado = {g : len(n) for g,n in d_asort.items()} 
plt.bar(dist_grado.keys(), dist_grado.values())
plt.show()
#%%
#Este último no es obligatorio, plotea todos los puntos de d_grados_vecinos en lugar del promedio. Es para chequear que el promedio tenga sentido
#Como hay varios valores por cada grado, uso [x]*len(n) para que haya la misma cantidad de x que de y
for x,y in d_grados_vecinos.items():
    plt.scatter([x]*len(y),y, color='b')
#%%
"Fiteo"
x = list(d_knn.keys())
y = list(d_knn.values())

lnx = np.log(x)
lny = np.log(y)

m, y0, r, p, std_err = stats.linregress(lnx,lny)
print(f'El exponente (mu) es = {m}')
plt.scatter(lnx,lny, color='b')
plt.plot(lnx, y0 + m*lnx, color='r')
plt.show()
#%%
""""item iv:
    En lugar de hacer la sumatoria grande, el libro de newmann me propone separarlo en
    varios pasos:
        S: = sum(kikj)-> sumar el producto kikj sobre tdos los pares de nodos i,j
        unidos por un enlace
        S1:  """
A = nx.adjacency_matrix(grafos['internet'], weight='value')

#%%
"S1 = 2*sum(kikj) donde ki,kj es el grado del nodo i,j y (i,j) es un enlace"

kikj = []
for i,j in edges:
    kikj.append(grado_propio[i]*grado_propio[j])

SL = sum

def S1(lista_enlaces):
    ki=[]
    for i,j in lista_enlaces:
        ki.append(grado_propio[i])
    return(sum(ki))

def S2(lista_enlaces):
    ki=[]
    for i,j in lista_enlaces:
        ki.append(grado_propio[i]**2)
    return(sum(ki))

def S3(lista_enlaces):
    ki=[]
    for i,j in lista_enlaces:
        ki.append(grado_propio[i]**3)
    return(sum(ki))
#%%
r = (S1*SL - S2**2)/(S1*S3 - S2**2)
