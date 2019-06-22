class Vertice:
    def __init__(self, pX, pY, id):
        self.pX = pX
        self.pY = pY
        self.regiao = 0
        self.id = id

    def setRegiao(self, regiao):
        self.regiao = regiao

    def getCoordenadas(self):
        return (self.pX, self.pY)

    def getId(self):
        return self.id
    
    def getRegiao(self):
        return self.regiao


class Grafo(Vertice):
    def __init__(self):
        self.vertices = []
        self.arestas = []
        self.cardV = 0

    def setArestas(self, matriz):
        self.arestas = matriz

    def getAresta(self, x, y):
        return self.arestas[x][y]
    
    def getConjArestas(self):
        return self.arestas

    def addVertice(self, x, y, id):
        self.vertices.append(Vertice(x, y, id))
        self.cardV += 1
    
    def addVerticePronto(self, v):
        self.vertices.append(v)
        self.cardV += 1
    
    def setRegiaoVertice(self, id, reg):
        id -= 1
        self.vertices[id].setRegiao(reg)

    def getVertice(self, id):
        id -= 1
        return self.vertices[id]
    
    def getCarV(self):
        return self.cardV

# class Grafo:
#     def __init__(self, arestas):
#         self.arestas = arestas
    
#     def getAresta(self, pos):
#         return self.arestas[pos]

# class Vertice:
#     def __init__(self, pX, pY, regiao):
#         self.pX = pX
#         self.pY = pY
#         self.regiao = regiao
    
#     def getRegi(self):
#         return self.regiao
    
#     def getCoordenada(self):
#         return (self.pX, self.pY)

#                                                 [Tarefa2: Algoritmo]
###########################################################################################################

#Passo 0: Algoritmo baseado em Trim para separação de subgrafos de acordo com a demanda e a capacidade
#de cada veiculo
import math

def subgrafosVeiculos(demandaRegiao, robotMap, confRegiao, g):
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
    '''
    # print()
    # print ("demandaTupla: ", demandaTupla)
    '''

    somatorio = 0
    for i in demandaRegiao:
        somatorio += i[1]
    capMinRobo = math.ceil(somatorio/robotMap[1])

    '''
    print("Somatorio: ", somatorio)
    print("Capacidade Minima veiculo: ", capMinRobo )
    '''

    #Algoritmo separa regiao para robos
    # if (robotMap[1] == 1):
    #     vetCapRobot = demandaTupla
    # else:
    vetCapRobot = []
    for i in range(robotMap[1]):
        capMinimaAtingida = False
        regioesVisita = []
        somatorioDemanda = 0
        demanda = 0

        # while capMinimaAtingida and len(demandaTupla) > demanda:
        if (robotMap[1] == 1):
            vetCapRobot = demandaTupla
        else:
            while ( (len(demandaTupla) > demanda)  and (not capMinimaAtingida)) :
                teste = somatorioDemanda + demandaTupla[demanda][1]
                if (teste <= capMinRobo):
                    somatorioDemanda += demandaTupla[demanda][1]
                    regioesVisita.append(demandaTupla[demanda])
                    del(demandaTupla[demanda])
                    demanda -= 1
                elif ((teste > capMinRobo+1) or (len(demandaTupla) < demanda)):
                    capMinimaAtingida = True

                demanda += 1

        vetCapRobot.append(regioesVisita)

    
    print (vetCapRobot)


    #Montando os subgrafos:
    subConjG = []
    for i in range(robotMap[1]):
        subConjG.append(Grafo())
        subConjG[i].setArestas(g.getConjArestas)

    j = 0
    for reg in vetCapRobot:
        for k in range(len(reg)):
            i = 1
            chave = reg[k][0]-1
            for i in range(len(confRegiao[chave])-1):
                subConjG[j].addVerticePronto(g.getVertice(confRegiao[chave][i]))
        j += 1

    for i in range(subConjG[0].cardV) :
        print(subConjG[0].getVertice(i).getId())

    return subConjG

#Passo 1: AGM Kruskall

    #                                       [Tarefa1: Extracao de dados]
 #######################################################################################################################
def main():

    import re

    robotMap = [] # robotMap[0]=qntVert robotMap[1]=qntVeic robotMap[2]=qntRegiao robotMap[3]=CapDeCaRobo
    coordenadas = [] # Coordenas de cada Vertices
    confRegiao = [] # regiao/vertices
    demandaRegiao = [] # Demanda de cada regiao

    with open('problema13.txt', 'r') as reader:
        
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
    '''
    # print("Detalhes: ", robotMap)
    # print("\n")

    # print("coordenadas:")
    # for linha in coordenadas:
    #     print(linha)

    # print("\n")
    # print("Configuracao de regiao:")
    # for linha in confRegiao:
    #     print (linha)

    # print("\n")
    # print("demandaRegiao:")
    # for linha in demandaRegiao:
    #     print(linha)

    # print("\nMatriz de distancias:\n")
    '''

    #                                              [Montagem do Grafo]
    #################################################################################################################

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

    '''
    #     distMatriz.append(linha)
    # for linha in distMatriz:
    #     for a in linha:
    #         print (a, end = "\t")
    #     print()
    '''

    #Criar grafo-------------------------------------------------------
    g = Grafo()

    #set id e coordenadas dos vertices:
    for item in coordenadas:
        g.addVertice(item[1], item[2], item[0])

    #set Regiao de cada vertice:
    for lista in confRegiao:
        i = 1
        while i < (len(lista)-1):
            g.setRegiaoVertice(lista[i], lista[0])
            i += 1

    #Adicionando arestas e pesos:
    g.setArestas(distMatriz)

    '''
    print("(x,y): ", g.getVertice(5).getCoordenadas())
    print("ID: ", g.getVertice(5).getId())
    print("Regiao: ", g.getVertice(5).getRegiao())
    '''
   

    #Desenhar grafo----------------------------------------------------
    # from igraph import *

    # grafo = Graph.Ring(len(coordenadas), circular=False)

    # layout = []
    # for vertice in coordenadas:
    #     x = vertice[1]
    #     y = vertice[2]
    #     layout.append((x,y))

    # arestas = []
    # for i in range(len(coordenadas)):
    #     j = i + 1 
    #     while j < len(coordenadas):
    #         arestas.append((i,j))
    #         j += 1

    # grafo.add_edges(arestas)

    # nome = []
    # for i in range(len(coordenadas)):
    #     nome.append(i + 1)

    # grafo.vs["name"] = nome

    #plot(grafo, layout = layout, bbox = (1000, 1000), margin = 0)

    subgrafosVeiculos(demandaRegiao, robotMap, confRegiao, g)

if __name__ == "__main__":
    main()

