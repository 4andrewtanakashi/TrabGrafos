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
    
    def setRegiaoVertice(self, pos, reg):
        pos -= 1
        self.vertices[pos].setRegiao(reg)

    def getVertice(self, pos):
        pos -= 1
        return self.vertices[pos]
    
    def getVerticeId(self, id):
        for v in self.vertices:
            if (v.getId() == id):
                return v
            
        return False
    
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

################################Passo 0: Algoritmo baseado em Trim para separação de subgrafos
#  de acordo com a demanda e a capacidade
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
    if (robotMap[1] == 1):
        vetCapRobot.append(demandaTupla)
    else:
        for i in range(robotMap[1]):
            capMinimaAtingida = False
            regioesVisita = []
            somatorioDemanda = 0
            demanda = 0

            # while capMinimaAtingida and len(demandaTupla) > demanda:
        
            
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
        subConjG[i].addVerticePronto(g.getVertice(1))
        subConjG[i].setArestas(g.getConjArestas())

    j = 0
    for reg in vetCapRobot:
        for k in range(len(reg)):
            i = 1
            chave = reg[k][0]-1
            while i < (len(confRegiao[chave])-1):
                subConjG[j].addVerticePronto(g.getVertice(confRegiao[chave][i]))
                i += 1
        j += 1

    #Seleciona apenas vertices e distancias do subgrafo
    listaDeTripla = []
    for qntSub in range(len(subConjG)):
        triplaRegUV = []
        for i in range(subConjG[qntSub].cardV) :
            j = i + 1
            while (j < (subConjG[qntSub].cardV)  ):
                u = subConjG[qntSub].getVertice(i).getId()
                v = subConjG[qntSub].getVertice(j).getId()
                u -= 1 #Para acessar Id no grafo é direto, mas acessar em uma ED é gaussiano
                v -= 1 #Para acessar Id no grafo é direto, mas acessar em uma ED é gaussiano
                triplaRegUV.append( (subConjG[qntSub].getConjArestas()[u][v], u+1, v+1) )
                j += 1
        #print("triplaRegUV", qntSub, ": ", triplaRegUV)
        listaDeTripla.append(triplaRegUV)

    for i in range(len(listaDeTripla)):
        subConjG[i].setArestas(listaDeTripla[i])

    '''
    for i in range(subConjG[qntSub].cardV) :
        print("v: ", subConjG[qntSub].getVertice(i).getId())
    '''
    #print("Tripla: ", triplaRegUV)
    '''
    print("TAM: ", len(subConjG))
    '''
    return subConjG




####################################################################Passo 1: AGM Kruskall
def kruskall(grafoG, robotMap, confRegiao):

    #1º Passo: Ordenação de pesos de arestas:
    grafoG.getConjArestas().sort(key=lambda x: x[0])
    print(grafoG.getConjArestas())
    #copyMatriz = grafoG.getConjArestas()
    #conjOrd = []
    #for i in range(len(copyMatriz[0])):
    #    j = i + 1
    #    while j < (len(copyMatriz[0])):
    #        conjOrd.append( (copyMatriz[i][j], i+1, j+1) )
    #        j = j+1
    #conjOrd.sort(key=lambda x: x[0])
    #print("Ordenação de peso: ", conjOrd)


    #2º Selecionar arestas de menor peso e nao coloca vértices pertencentes ao mesmo conjunto 
    #e elimina vertices que estão com o mesma regiao .
    conjKruskall = []
    conjEliminados = []
    for tripla in grafoG.getConjArestas():

        #1ª Consulta u.regiao != v.regiao
        if ( (grafoG.getVerticeId(tripla[1]).getRegiao()) != (grafoG.getVerticeId(tripla[2]).getRegiao()) ):
            naoEstaPresente = True

            for elim in conjEliminados:
                if (tripla[1] == elim):
                    naoEstaPresente = False

            for elim in conjEliminados:
                if (tripla[2] == elim) :
                    naoEstaPresente = False

            #2ª u ou v estao como eliminados
            if (naoEstaPresente == False):
                estaKruskall = 0
                verDaTupla = 0
                verticeNaoIncluido = 0

                for tupla in conjKruskall:
                    for verTup in tupla:
                        if (tripla[1] == verTup):
                            estaKruskall += 1
                            verDaTupla = tripla[2]
                            verticeNaoIncluido = tripla[1]

                for tupla in conjKruskall:
                    for verTup in tupla:
                        if (tripla[2] == verTup):
                            estaKruskall += 1
                            verDaTupla = tripla[1]
                            verticeNaoIncluido = tripla[2]

                #3º se estao no conjunto Kruskall:
                if (krus <= 1) :
                    #Em caso dos dois vertices nao estarem subconjunto
                    if (estaKruskall == 0):
                        uId = grafoG.getVerticeId(tripla[1]).getId()
                        vId = grafoG.getVerticeId(tripla[2]).getId()
                        conjKruskall.append((uId, vId))

                        regiao1 = grafoG.getVerticeId(tripla[1]).getRegiao()
                        regiao2 = grafoG.getVerticeId(tripla[2]).getRegiao()
                        
                        i = 1
                        while i < (len(confRegiao[regiao1])-1):
                            idEli = confRegiao[regiao1][i]
                            conjEliminados.append(idEli)
                            i += 1
                        
                        i = 1
                        while i < (len(confRegiao[regiao2])-1):
                            idEli = confRegiao[regiao2][i]
                            conjEliminados.append(idEli)
                            i += 1

                    #Em caso de um vertice nao estar subconjunto
                    #PAROU AQUI !!!!
                    else :
                        posTupla = 0
                        for conjLig in conjKruskall:
                            i = 0
                            for ele in len(conjLig) :
                                if (conjLig[i] == verDaTupla):
                                    posTupla = i

                        conjKruskall.append(arestaComparacao) 
                        regiao = grafoG.getVerticeId(arestaComparacao).getRegiao()


                        i = 1
                        while i < (len(confRegiao[regiao])-1):
                            idEli = confRegiao[regiao][i]
                            conjEliminados.append(idEli)
                            i += 1
#    k = 0
#    insere = 0
#    while (len(conjVer) != robotMap[0]) and (k < len(conjOrd)):

#        u = 0
#        for i in range(2):
#            for j in range(len(conjVer)):
#                if (conjOrd[k][i] == conjVer[j]):
#                    insere += 1
#                    u = conjVer[j]

#        if (insere == 0):
#            conjVer.append(conjOrd[k][1])
#            conjVer.append(conjOrd[k][2])
#            conjPosAres.append(k)
#        elif (insere == 1):
#            conjVer.append(u)
#            conjPosAres.append(k)
#            insere = 0

       # k = k+1 

##################################################################################################################



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

        distMatriz.append(linha)

    '''
    for linha in distMatriz:
        for a in linha:
            print (a, end = "\t")
        print()
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

    subG = subgrafosVeiculos(demandaRegiao, robotMap, confRegiao, g)
    kruskall(subG[0], robotMap, confRegiao)
    #for i in range(len(subG)):
    #    subG[i] = kruskall(subG[i])


if __name__ == "__main__":
    main()