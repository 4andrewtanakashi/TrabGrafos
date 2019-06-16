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

#>>> matriz = [ [1, 2, 3, 4], [1, 2, 3, 4] ]
# >>> matriz[0][0]
# 1
# >>> matriz[0][0] = 3
# >>> matriz[0][0]
#3