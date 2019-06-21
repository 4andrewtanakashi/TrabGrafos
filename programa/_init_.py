class Vertice:
    def __init__(self, pX, pY, regiao, id):
        self.pX = pX
        self.pY = pY
        self.regiao = regiao
        self.id = id
    
    def getCoordenadas(self):
        return (self.pX, self.pY)

    def getId(self):
        return self.id
    
    def getRegiao(self):
        return self.regiao

class Grafo:
    def __init__(self, arestas):
        self.arestas = arestas
    
    def getAresta(self, pos):
        return self.arestas[pos]

import re

class Vertice:
    def __init__(self, pX, pY, regiao):
        self.pX = pX
        self.pY = pY
        self.regiao = regiao
    
    def getRegi(self):
        return self.regiao
    
    def getCoordenada(self):
        return (self.pX, self.pY)


robotMap = []
coordenadas = []
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
        coordenadas.append(numbers)
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
for linha in coordenadas:
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
for nPtoA in range(len(coordenadas)):
    linha = []
    for nPtoB in range(len(coordenadas)):
        xA = coordenadas[nPtoA][1]
        xB = coordenadas[nPtoB][1]
        yA = coordenadas[nPtoA][2]
        yB = coordenadas[nPtoB][2]

        calcDistancia = round(dist(xA,xB,yA,yB), 3)

        linha.append(calcDistancia)

    distMatriz.append(linha)
for linha in distMatriz:
    for a in linha:
        print (a, end = "\t")
    print()

#Criar grafo-------------------------------------------------------



#Desenhar grafo----------------------------------------------------
from igraph import *

grafo = Graph.Ring(len(coordenadas), circular=False)

layout = []
for vertice in coordenadas:
    x = vertice[1]
    y = vertice[2]
    layout.append((x,y))

arestas = []
for i in range(len(coordenadas)):
    j = i + 1 
    while j < len(coordenadas):
        arestas.append((i,j))
        j += 1

grafo.add_edges(arestas)

nome = []
for i in range(len(coordenadas)):
    nome.append(i + 1)

grafo.vs["name"] = nome

#plot(grafo, layout = layout, bbox = (1000, 1000), margin = 0)

#Ordenacao Demanda--------------------------------------------
"""
    Faz ordenação  das regioes: da regiao com menor demada
    para a maior
"""
demandaTupla = []
for i in demandaRegiao:
    a = (i[0],i[1])
    demandaTupla.append(a)

demandaTupla.sort(key=lambda x: x[1])
demandaTupla.reverse()
print()
print (demandaTupla)