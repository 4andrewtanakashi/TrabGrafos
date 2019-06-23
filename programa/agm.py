import re

class Vertice:
    def __init__(self, pX, pY, peso):
        self.pX = pX
        self.pY = pY
        self.peso = peso
    
    def getPeso(self):
        return self.peso
    
    def getCoordenada(self):
        return (self.pX, self.pY)


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

#print("\nMatriz de distancias:\n")

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

#for linha in distMatriz:
#    for a in linha:
#        print (a, end = "\t")
#    print()



#1º Passo: Ordenação de pesos de arestas:

conjOrd = []
for i in range(len(distMatriz[0])):
    j = i + 1
    while j < (len(distMatriz[0])):
        conjOrd.append( (distMatriz[i][j], i+1, j+1) )
        j = j+1
conjOrd.sort(key=lambda x: x[0])

print("Ordenação de peso: ", conjOrd)

#2º Selecionar arestas de menor peso e não coloca vértices pertencentes ao mesmo conjunto 
#e elimina vertices que estão com o mesmo peso .
conjVer = []
conjPosAres = []
k = 0
insere = 0
while (len(conjVer) != robotMap[0]) and (k < len(conjOrd)):

    u = 0
    for i in range(2):
        for j in range(len(conjVer)):
            if (conjOrd[k][i] == conjVer[j]):
                insere += 1
                u = conjVer[j]

    if (insere == 0):
        conjVer.append(conjOrd[k][1])
        conjVer.append(conjOrd[k][2])
        conjPosAres.append(k)
    elif (insere == 1):
        conjVer.append(u)
        conjPosAres.append(k)
        insere = 0

    k = k+1

#print("\n \n ")
#print(conjVer)

#for i in range(len(conjPosAres)):
#    print("Arestas: ", "(", conjOrd[conjPosAres[i]][1], ",", conjOrd[conjPosAres[i]][2], ")")


