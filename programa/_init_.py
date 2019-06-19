import re
#import igraph

robotMap = []
coordenandas = []
confRegiao = []
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
print("coordenadas: ", coordenandas)
print("\n")
print("Configuracao de regiao: ", confRegiao)
print("\n")
print("demandaRegiao: ", demandaRegiao)

print("\n-------------------------------\n")
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
    print (linha)
