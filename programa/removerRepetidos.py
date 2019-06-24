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

    #------------------------------------------------------------------
    def getVertices(self):
        return self.vertices
    #------------------------------------------------------------------
    
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
    
    def getVerticeId(self, id):
        for v in self.vertices:
            if (v.getId() == id):
                return v
        #print("AQUI: ", id) 
        return False
    
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


def removerRepetidos (grafo):
    vertices = grafo.getVertices()
    posA = 1

    remover = []
    while posA < (len(vertices) - 1):
        for posB in range(len(vertices)):
            if pos != i:
                if vertices[posA] == vertices[posB]:
                    remover.append[posB]
    
    for posRemover in remover:
        removeId = vertices[posRemover].getId
        grafo.delVertiveId(removeId)
        
        verticeAntes = vertices[posRemover - 1]
        verticeAntesX = verticeAntes.getCoordenadas()[0]
        verticeAntesY = verticeAntes.getCoordenadas()[1]

        verticeDepois = vertices[posRemover + 1]
        verticeDepoisX = verticeDepois.getCoordenadas()[0]
        verticeDepoisY = verticeDepois.getCoordenadas()[1]

        verticeRemover = vertices[posRemover]
        verticeRemoverX = verticeRemover.getCoordenadas()[0]
        verticeRemoverY = verticeRemover.getCoordenadas()[1]

        distAntes = dist(verticeAntesX, verticeRemoverX, verticeAntesY, verticeRemoverY)
        arestaAntes = (distAntes, verticeAntes, verticeRemover)

        distDepois = dist(verticeDepoisX, verticeRemoverX, verticeDepoisY, verticeRemoverY)
        arestaDepois = (distDepois, verticeDepois, verticeRemover)

        grafo.delAresta(arestaAntes)
        grafo.delAresta(arestaDepois)

        distNovaAresta = dist(verticeAntesX, verticeDepoisX, verticeAntesY, verticeDepoisY)
        novaAresta = (distNovaAresta, verticeAntes, verticeDepois)

        grafo.setAresta(novaAresta)

    return grafo