# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 12:03:25 2020

@author: usuario
"""

from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
import itertools as it

#%%
red_3 = nx.lollipop_graph(21,5)
diam = nx.diameter(red_3)
med = nx.average_shortest_path_length(red_3)
print(f'el diametro es {diam} y la distancia media es {med}')
nx.draw(red_3, with_labels = True)
plt.show()
#%%
"""Creador de enlaces"""

def panadero(k,p):
    """hace una red con forma de panadero
    con una cadena k nodos y p cositos en la punta"""
    cadena = list(zip(range(1,k),range(2,k+1)))
    globo = list(zip(it.repeat(k,p), range(k+1,k+1+p)))
    pan = nx.Graph()
    pan.add_edges_from(cadena+globo)
    nx.draw(pan, with_labels=True)
    diam = nx.diameter(pan)
    med = nx.average_shortest_path_length(pan)
    print(f'El diametro de la red es {diam} y la distancia media es {med}')
    plt.show()

#%%
k = 6
cadena = list(zip(range(1,k),range(2,k+1)))
tuplas = list(cadena + [(k,1)])

anillo = nx.Graph()
anillo.add_edges_from(tuplas)
nx.draw(anillo, with_labels = True)
plt.show()
