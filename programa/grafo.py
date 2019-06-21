class Vertice:
    def __init__(self, pX, pY, peso, id):
        self.pX = pX
        self.pY = pY
        self.peso = peso
        self.id = id
    
    def getPeso(self):
        return self.peso
    
    def getCoordenadas(self):
        return (self.pX, self.pY)

    def getId(self):
        return self.id
    
    def setPeso(self, p):
        self.peso = p

    def setCoordenadas(self, x, y):
        self.px = x
        self.py = y



class Grafo(object):

    contadorId = 1

    def __init__(self):
        self.arestas = []
        self.vertices = []
        self.cardV = 0


    def addVertices (self, qntVer) :
        self.cardV = self.cardV + qntVer
        i = 0
        while i < qntVer:
            self.vertices.append(Vertice(0, 0, 0, self.contadorId))
            
            i += 1
            self.contadorId += 1
        
    
    def addAresta (self, arestas):
        for i in arestas:
            self.arestas.append(i)


    def getVertice (self, contadorId):
        return self.vertices[contadorId]

    def setV (self, contadorId, x, y, peso):
        self.vertices[contadorId].setPeso(peso)
        self.vertices[contadorId].setCoordenadas(x, y)

    def _print_(self):
        for i in self.vertices:
            print("(x, y): ", i.getCoordenadas() )
            print("id: ", i.getId() )
            print("peso: ", i.getPeso() )

        print(self.arestas)

    @classmethod
    def all(cls):
        return cls.objects

g = Grafo()
g.addVertices(5)
g.addAresta([(1,2), (2,1)])
g._print_()
