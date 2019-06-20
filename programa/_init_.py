import re
#import igraph

robotMap = []
coordenandas = []
confRegiao = [] #preencher
demandaRegiao = []

# file = open('problema15.txt', 'r')
# for i in file:
with open('problema15.txt', 'r') as reader:
    
    linha = reader.readline()
    while ( not ('SECTION' in linha ) ):
        if ( (not ('EDGE' in linha)) ):
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", linha )
            robotMap.append(int(numbers[0]))
        linha = reader.readline()

    linha = reader.readline()
    while ( not ('SET_SECTION' in linha) ):
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", linha )
        numbers = [int(i) for i in numbers]
        coordenandas.append(numbers)
        linha = reader.readline()

    linha = reader.readline()
    while ( not ('DEMAND_SECTION' in linha) ):
        numbers = re.findall(r"[+]?\d*\.\d+|\d+", linha )
        numbers = [int(i) for i in numbers]
        confRegiao.append(numbers)
        linha = reader.readline()

    linha = reader.readline()
    while ( linha != 'EOF' ):
        numbers = re.findall(r"[+]?\d*\.\d+|\d+", linha )
        numbers = [int(i) for i in numbers]
        demandaRegiao.append(numbers)
        linha = reader.readline()

    reader.close()


print("Detalhes: ", robotMap)
print("\n")

print("coordenadas:")
for linha in coordenandas:
    print(linha)

print("\n")
print("Configuracao de regiao:")
for linha in confRegiao:
    print (linha)

print("\n")
print("demandaRegiao:")
for linha in demandaRegiao:
    print(linha)

print("\nMatriz de distancias:\n")

#Matriz distancia--------------------------------------------------
def dist (xA, xB, yA, yB):
    distancia = (((xA - xB) ** 2) + ((yA - yB) ** 2)) ** (1/2)
    return distancia

distMatriz = []
for nPtoA in range(len(coordenandas)):
    linha = []
    for nPtoB in range(len(coordenandas)):
        xA = coordenandas[nPtoA][1]
        xB = coordenandas[nPtoB][1]
        yA = coordenandas[nPtoA][2]
        yB = coordenandas[nPtoB][2]

        calcDistancia = round(dist(xA,xB,yA,yB), 3)

        linha.append(calcDistancia)

    distMatriz.append(linha)

for linha in distMatriz:
    for a in linha:
        print (a, end = "\t")
    print()

#Desenhar grafo----------------------------------------------------
from igraph import *

grafo = Graph.Ring(len(coordenandas), circular=False)

layout = []
for vertice in coordenandas:
    x = vertice[1]
    y = vertice[2]
    layout.append((x,y))

arestas = []
for i in range(len(coordenandas)):
    j = i + 1 
    while j < len(coordenandas):
        arestas.append((i,j))
        print((i,j), end = " ")
        j += 1
        
    print()
grafo.add_edges(arestas)

nome = []
for i in range(len(coordenandas)):
    nome.append(i + 1)

grafo.vs["name"] = nome

plot(grafo, layout = layout, bbox = (1000, 1000), margin = 0)