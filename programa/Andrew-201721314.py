import re # Para extrair apenas numeros dos arquivos
import math #Para usar ceil
import sys #Para pegar o maior valor possivel
import time #Medr tempo de execucao
 # from igraph import *

class Vertice:
    def __init__(self, pX, pY, id, gr):
        self.pX = pX
        self.pY = pY
        self.regiao = 0
        self.id = id
        self.grau = gr

    def setRegiao(self, regiao):
        self.regiao = regiao

    def getCoordenadas(self):
        return (self.pX, self.pY)

    def getId(self):
        return self.id
    
    def getRegiao(self):
        return self.regiao
    
    def setGrau(self, d):
        self.grau = d
    
    def getGrau(self):
        return self.grau

class Grafo(Vertice):
    def __init__(self):
        self.vertices = []
        self.arestas = []
        self.cardV = 0

    def setArestas(self, matriz):
        self.arestas = matriz
    
    def setAresta(self, a):
        self.arestas.append(a)
    
    def delAresta(self, a):
        self.arestas.remove(a)

    def getAresta(self, x, y):
        return self.arestas[x][y]
    
    def getConjArestas(self):
        return self.arestas
    
    def buscaAresta(self, tripla):
        for e in self.arestas:
            if ((e[1], e[2]) == (tripla[1], tripla[2]) ):
                return True
            elif ((e[2], e[1]) == (tripla[1], tripla[2])):
                return True

    def addVertice(self, x, y, id, gr):
        self.vertices.append(Vertice(x, y, id, gr))
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
    
    def getVertices(self):
        return self.vertices
    
    def getVerticeId(self, id):
        for v in self.vertices:
            if (v.getId() == id):
                return v
        return False

    def setConjVert(self, listaV):
        self.vertices = listaV
    
    def getCarV(self):
        return self.cardV
    
    def delVertiveId(self, id):
        pos = -1
        i = 0
        while ((i < len(self.vertices)) and (pos == -1)):
            if (self.vertices[i].getId() == id):
                pos = i
            i += 1
        if (pos != -1):
            del self.vertices[pos]
            self.cardV -= 1

    def setGrauVert(self, id, grau):
        self.getVerticeId(id).setGrau(grau)
    
    def aumentarGrau(self, id):
        grau = self.getVerticeId(id).getGrau()
        grau += 1
        self.getVerticeId(id).setGrau(grau)


def dist (xA, xB, yA, yB):
        distancia = (((xB - xA) ** 2) + ((yB - yA) ** 2)) ** (1/2)
        return distancia


#                                                 [Tarefa2: Algoritmo]
###########################################################################################################

################################Passo 0: Algoritmo baseado em Trim para separação de subgrafos
#  de acordo com a demanda e a capacidade
#de cada veiculo


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
    

    #Algoritmo separa regiao para robos
    vetCapRobot = []
    if (robotMap[1] == 1):
        vetCapRobot.append(demandaTupla)
    else:
        for i in range(robotMap[1]):
            capMinimaAtingida = False
            regioesVisita = []
            somatorioDemanda = 0
            demanda = 0


            while ( (len(demandaTupla) > demanda)  and (not capMinimaAtingida)) :
                teste = somatorioDemanda + demandaTupla[demanda][1]
                if (teste <= robotMap[3]):
                    somatorioDemanda += demandaTupla[demanda][1]
                    regioesVisita.append(demandaTupla[demanda])
                    del(demandaTupla[demanda])
                    demanda -= 1
                   
                elif (( (len(demandaTupla)-1) == demanda )):
                   
                    capMinimaAtingida = True
                elif (((teste - demandaTupla[demanda][1]) < robotMap[3]+1)):
                    restante = robotMap[3] - somatorioDemanda
                    satisfeito = False
                    ind = 0
                    while (ind < (len(demandaTupla)-1) and (not satisfeito)):
                        if (demandaTupla[ind][1] <= restante):
                            
                            somatorioDemanda += demandaTupla[ind][1]
                            regioesVisita.append(demandaTupla[ind])
                            demandaTupla.remove(demandaTupla[ind])
                            demanda -= 1
                            satisfeito = True
                        ind += 1
                demanda += 1
                

            vetCapRobot.append(regioesVisita)

  
    #Montando os subgrafos:
    subConjG = []
    for i in range(robotMap[1]):
        subConjG.append(Grafo())
        subConjG[i].addVerticePronto(g.getVertice(1)) #Todos os subgrafos recebem o v1
        subConjG[i].setArestas(g.getConjArestas())

    j = 0
    for reg in vetCapRobot:
        for k in range(len(reg)):
            i = 1
            chave = reg[k][0]-1
            while i < (len(confRegiao[chave])-1):
                subConjG[j].addVerticePronto(g.getVertice(confRegiao[chave][i]))
                subConjG[j].setGrauVert(confRegiao[chave][i], subConjG[j].cardV)
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
     
        listaDeTripla.append(triplaRegUV)

    for i in range(len(listaDeTripla)):
        subConjG[i].setArestas(listaDeTripla[i])

    vetQntRegiao = []
    for robo in vetCapRobot:
        vetQntRegiao.append(len(robo))

    return (subConjG, vetQntRegiao)




####################################################################Passo 1: AGM Kruskall
def kruskall(grafoG, robotMap, confRegiao, qntRegiao, distMatriz):

    #1º Passo: Ordenação de pesos de arestas:
    grafoG.getConjArestas().sort(key=lambda x: x[0])


    #2º Selecionar arestas de menor peso e nao coloca vértices pertencentes ao mesmo conjunto 
    #e elimina vertices que estão com o mesma regiao .
    conjKruskall = []
    conjEliminados = []
    conjArestasAgm = []
    agm = False
    count = 0

    while ( (count < len(grafoG.getConjArestas())) and (agm == False)):
        tripla = grafoG.getConjArestas()[count]
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
            if (naoEstaPresente == True):
                estaKruskall = 0
                posicaoTupla = None
                posicaoTupla2 = None
                verticeNaoIncluido = 0
                
                tupla1 = 0
                posTupKrus = 0
                while (posTupKrus < len(conjKruskall)) :
                    for verTup in conjKruskall[posTupKrus]:
                        if (tripla[1] == verTup):
                            estaKruskall += 1
                            posicaoTupla = posTupKrus
                            verticeNaoIncluido = tripla[2]
                           
                            tupla1 = conjKruskall[posTupKrus]
                    posTupKrus += 1

                tupla2 = 1
                posTupKrus = 0
                while (posTupKrus < len(conjKruskall)) :
                    for verTup in conjKruskall[posTupKrus]:
                        if (tripla[2] == verTup):
                            estaKruskall += 1
                            posicaoTupla2 = posTupKrus
                            verticeNaoIncluido = tripla[1]
                            
                            tupla2 = conjKruskall[posTupKrus]
                    posTupKrus += 1
                
                if (tupla1 == tupla2):
                    estaKruskall += 1

                #3º se estao no conjunto Kruskall:
                if (estaKruskall <= 2) :
                    #Em caso dos dois vertices nao estarem subconjunto
                    if (estaKruskall == 0):
                        conjKruskall.append((tripla[1], tripla[2]))
                        conjArestasAgm.append((tripla[1], tripla[2]))
                        

                        regiao1 = grafoG.getVerticeId(tripla[1]).getRegiao()
                        regiao2 = grafoG.getVerticeId(tripla[2]).getRegiao()
                        
                        regiao1 -= 1 #Pega os ids certos, mas para acessar o vetor e pos gaussiano
                        regiao2 -= 1 #Pega os ids certos, mas para acessar o vetor e pos gaussiano

                        unicaTupla = conjKruskall[0]
                        t = 1
                        while (t < len(conjKruskall)):
                            unicaTupla = unicaTupla + conjKruskall[t]
                            t += 1

                        i = 1
                        while i < (len(confRegiao[regiao1])-1):
                            idEli = confRegiao[regiao1][i]
                            if ((tripla[1] != idEli) and ( not (idEli in conjEliminados) ) and (not (idEli in unicaTupla) )):
                                conjEliminados.append(idEli)
                            i += 1

                        i = 1
                        while i < (len(confRegiao[regiao2])-1):
                            idEli = confRegiao[regiao2][i]
                            if (tripla[2] != idEli and ( not (idEli in conjEliminados)) and (not (idEli in unicaTupla) )):
                                conjEliminados.append(idEli)
                            i += 1

                    #Em caso de um vertice nao estar subconjunto:
                    if (estaKruskall == 1) :
                        
                        if (not (posicaoTupla is None)):
                      
                            tupTemp = conjKruskall[posicaoTupla] + (verticeNaoIncluido,)
                            del conjKruskall[posicaoTupla]
                            conjKruskall.append(tupTemp)
                            conjArestasAgm.append((tripla[1], verticeNaoIncluido))

                        else:
                           
                            tupTemp = conjKruskall[posicaoTupla2] + (verticeNaoIncluido,)
                            del conjKruskall[posicaoTupla2]
                            conjKruskall.append(tupTemp)
                            conjArestasAgm.append((tripla[2], verticeNaoIncluido ))

                        unicaTupla = conjKruskall[0]
                        t = 1
                        while (t < len(conjKruskall)):
                            unicaTupla = unicaTupla + conjKruskall[t]
                            t += 1

                        regiao = grafoG.getVerticeId(verticeNaoIncluido).getRegiao()
                        regiao -= 1 #Pega os ids certos, mas para acessar o vetor e pos gaussiano
                        i = 1
                        while i < (len(confRegiao[regiao])-1):
                            idEli = confRegiao[regiao][i]
                            if (verticeNaoIncluido != idEli and (not (idEli in conjEliminados)) and (not (idEli in unicaTupla) )):
                                
                                conjEliminados.append(idEli)
                            i += 1
                    
                    #Em caso dos vertices estarem em dois conjuntos diferentes (uniao de conjunto)
                    if (estaKruskall == 2):
                        
                        conjArestasAgm.append((tripla[1], tripla[2]))

                        tupTemp = conjKruskall[posicaoTupla] + conjKruskall[posicaoTupla2]
                        
                        if (posicaoTupla < posicaoTupla2):
                            posicaoTupla2 -= 1

                        del conjKruskall[posicaoTupla]
                        del conjKruskall[posicaoTupla2] #Como é uma lista o indice fica em uma pos-1
                        conjKruskall.append(tupTemp)
            
        count += 1

        if (len(conjKruskall) == 1):
            krus = tuple(conjKruskall[0])
            if ( (len(krus)-1) == qntRegiao):
                
                agm = True
    
    for v in conjEliminados:
        grafoG.delVertiveId(v)


    arestasAgm = []
    for eleTupla in conjArestasAgm:
        u = eleTupla[0]
        v = eleTupla[1]
        u -= 1 #Para acessar Id no grafo é direto, mas acessar em uma ED é gaussiano
        v -= 1 #Para acessar Id no grafo é direto, mas acessar em uma ED é gaussiano
        arestasAgm.append( (distMatriz[u][v], u+1, v+1) )
        grafoG.setGrauVert(u+1, 0)
        grafoG.setGrauVert(v+1, 0)
    grafoG.setArestas(arestasAgm)

   
    for tup in conjArestasAgm:
        for v in tup:
            grafoG.aumentarGrau(v)
    

    return grafoG



###############################################################################################################
#                                   [2ºPasso Casamento Perfeito]:

def casamentoPerfeito(agm, distMatriz):

    #Pega Vertices de grau impar
    listaVertGrauImpar = []
    for i in range(agm.getCarV()):
        if ((agm.getVertice(i).getGrau())%2 == 1 ):
            listaVertGrauImpar.append(agm.getVertice(i).getId())

    #Organizar em subconjuntos possiveis ligacoes:
    i = 0
    listaPossLig = []
    while i < len(listaVertGrauImpar):
        j = i+1
        while j < len(listaVertGrauImpar):
            triplaImpar = (distMatriz[listaVertGrauImpar[i]-1][listaVertGrauImpar[j]-1], listaVertGrauImpar[i], listaVertGrauImpar[j])
            triplaImpar2 = (triplaImpar[0], triplaImpar[2], triplaImpar[1]) 
            if (not agm.buscaAresta(triplaImpar)) and (not(agm.buscaAresta(triplaImpar2))):
                if (not triplaImpar in listaPossLig):
                    listaPossLig.append(triplaImpar)
            j += 1
        i += 1
    
    #NOVO
    tamConj = len(listaVertGrauImpar)

    listaArestasDoCasa = []
    menorValor = sys.maxsize # Maior valor possivel
    backup = 0
    if (listaPossLig != []):
        elerm = listaPossLig[0]
    while ( listaPossLig != []  ) :

        for ele in listaPossLig:
       
            if (ele[0] < menorValor):
                elerm = ele
                menorValor = ele[0]

        if (backup != menorValor):
            listaArestasDoCasa.append(elerm)
            agm.aumentarGrau(elerm[1])
            agm.aumentarGrau(elerm[2])
            backup = menorValor

        menorValor = sys.maxsize
        i = 0
        while ((listaPossLig != []) and (i < len(listaPossLig))):
            if ( (listaPossLig[i][1] == elerm[1]) or ((listaPossLig[i][2] == elerm[1]))):
                listaPossLig.remove(listaPossLig[i])
                if (listaPossLig != []):
                    #NOVO
                    i = -1
            elif ( (listaPossLig[i][1] == elerm[2]) or ((listaPossLig[i][2] == elerm[2]))):
                listaPossLig.remove(listaPossLig[i])
                if (listaPossLig != []):
                    #NOVO
                    i = -1
            i += 1
    
    #NOVOs
    listaVertGrauImpar = []
    if ((tamConj/2) != len(listaArestasDoCasa)):
        for i in range(agm.getCarV()):
            if ((agm.getVertice(i).getGrau())%2 == 1 ):
                listaVertGrauImpar.append(agm.getVertice(i).getId())
        j = 0
        k = j+1 
        while (listaVertGrauImpar != []) :
            triplaImpar = (distMatriz[listaVertGrauImpar[j]-1][listaVertGrauImpar[k]-1], listaVertGrauImpar[j], listaVertGrauImpar[k])
            listaArestasDoCasa.append(triplaImpar)
            agm.aumentarGrau(triplaImpar[1])
            agm.aumentarGrau(triplaImpar[2])
            listaVertGrauImpar.remove(triplaImpar[1])
            listaVertGrauImpar.remove(triplaImpar[2])
            j = 0
            k = j+1
    ###

    for a in listaArestasDoCasa:
        agm.setAresta(a)
   
    return agm 


##################################################################################################################

######################################################[CircuitoEuleriano]########################
def circuitoEuleriano (eulerG):
   
    ordArestas = []
    for n in eulerG.getConjArestas(): # Python as variaveis recebem referencias e nao copia uma ED por atriuicao
        ordArestas.append(n)
    ordArestas.sort(key = lambda x: x[1])

    circuitoEuler = []
    circuitoEuler.append(ordArestas[0][1])
    buscar = ordArestas[0][2]
    verInicio = ordArestas[0][1]
    del ordArestas[0]

    while ((ordArestas != [])):
        i = 0
        while ( i < len(ordArestas)):
            if (buscar == ordArestas[i][1]) :
                circuitoEuler.append(buscar)
                buscar = ordArestas[i][2]
                
                del ordArestas[i]
            elif (buscar == ordArestas[i][2]):
                circuitoEuler.append(buscar)
                buscar = ordArestas[i][1]
                del ordArestas[i]
           #NOVO
            elif ((buscar == verInicio) and ((ordArestas) != [])):
                 buscar = ordArestas[0][1]
                 verInicio = buscar 
            i += 1
    circuitoEuler.append(verInicio)
    
    
    eulerG.setConjVert(circuitoEuler)
   
    
    return eulerG

##########################################################################

######################################[Passo ultimo: remover]##############################################################

def removerRepetidos (grafo, distM):
    vertices = grafo.getVertices()

    conj = set()
    unicos = []
    for v in vertices:
        if v not in conj:
            unicos.append(v)
            conj.add(v)
    
    unicos.append(vertices[0])
    grafo.setConjVert(unicos)

    listaVert = grafo.getVertices()
    listaAresta = []
    somatorioCusto = 0
    for i in range(len(listaVert)):
        j = i+1
        if (j < len(listaVert)):
            listaAresta.append((distM[listaVert[i]-1][listaVert[j]-1], listaVert[i], listaVert[j]))
            somatorioCusto += distM[listaVert[i]-1][listaVert[j]-1]
            
    grafo.setAresta(listaAresta)

    return (grafo, somatorioCusto)

########################################################################################################################


    

    #                                       [Tarefa1: Extracao de dados]
 #######################################################################################################################
def main():
    inicio = time.time()
    robotMap = [] # robotMap[0]=qntVert robotMap[1]=qntVeic robotMap[2]=qntRegiao robotMap[3]=CapDeCaRobo
    coordenadas = [] # Coordenas de cada Vertices
    confRegiao = [] # regiao/vertices
    demandaRegiao = [] # Demanda de cada regiao

    nomeArq = "problema"
    numArq = input("Digite o numero do problema do arquivo: ")
    with open(nomeArq+numArq+'.txt', 'r') as reader:
        nomeArq += numArq

        linha = reader.readline()
        while ( not ('SECTION' in linha ) ):
            if ( (not ('EDGE' in linha)) ):
                numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", linha )
                robotMap.append(int(numbers[0]))
            linha = reader.readline()

        linha = reader.readline()
        while ( not ('SET_SECTION' in linha) ):
            numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", linha )
            numbers = [int(i) for i in numbers]
            coordenadas.append(numbers)
            linha = reader.readline()

        linha = reader.readline()
        while ( not ('DEMAND_SECTION' in linha) ):
            numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", linha )
            numbers = [int(i) for i in numbers]
            confRegiao.append(numbers)
            linha = reader.readline()

        linha = reader.readline()
        while ( linha != 'EOF' ):
            numbers = re.findall(r"[+-]?\d+(?:\.\d+)?", linha )
            numbers = [int(i) for i in numbers]
            demandaRegiao.append(numbers)
            linha = reader.readline()

        reader.close()


    #                                              [Montagem do Grafo]
    #################################################################################################################

    #Matriz distancia--------------------------------------------------
    

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


    #Criar grafo-------------------------------------------------------
    g = Grafo()

    #set id e coordenadas dos vertices:
    for item in coordenadas:
        g.addVertice(item[1], item[2], item[0], robotMap[0])

    #set Regiao de cada vertice:
    for lista in confRegiao:
        i = 1
        while i < (len(lista)-1):
            g.setRegiaoVertice(lista[i], lista[0])
            i += 1

    #Adicionando arestas e pesos:
    g.setArestas(distMatriz)

    resulTupla = subgrafosVeiculos(demandaRegiao, robotMap, confRegiao, g)
    subG = resulTupla[0]
    vetQntReg = resulTupla[1]

    agm = []
    casPer = []
    listCir = []
    hamil = []
    custo = 0
    for i in range(len(subG)):
        tempFor = kruskall(subG[i], robotMap, confRegiao, vetQntReg[i], distMatriz)
        agm.append(tempFor)

        tempFor1 = casamentoPerfeito(agm[i], distMatriz)
        casPer.append(tempFor1)
       

        tempFor2 = circuitoEuleriano(casPer[i])
        listCir.append(tempFor2)

        tempFor4 = removerRepetidos(listCir[i], distMatriz)
        custo += tempFor4[1]
        hamil.append(tempFor4[0])
    
  
    for i in listCir:
        print(i.vertices)
    
    fim = time.time()
    print(nomeArq, "",custo, "", fim - inicio)


if __name__ == "__main__":
    main()