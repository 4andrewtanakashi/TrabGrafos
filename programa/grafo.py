class Vertice:
    def __init__(self, pX, pY, peso):
        self.pX = pX
        self.pY = pY
        self.peso = peso
    
    def getPeso(self):
        return self.peso
    
    def getCoordenada(self):
        return (self.pX, self.pY)
    
    def setPeso(self, p):
        self.peso = p

    def setCoordenadas(self, x, y):
        self.px = x
        self.py = y

class Grafo(Vertice, object):

    id = 1

    def __init__(self):
        self.arestas = []
        self.vertices = []
        self.cardV = 0


    def addVertices (self, qntVer) :
        self.cardV = self.cardV + qntVer
        i = 0
        while i < qntVer:
            self.vertices.append(super(Grafo, self).__init__(0,0,0))
            self.id = self.id
            i += 1
            self.id += 1
        
    
    def addAresta (self, arestas):
        for i in arestas:
            self.arestas.append(i)


    def getVertice (self, id):
        return self.vertices[id]

    def setV (self, id, x, y, peso):
        self.vertices[id].setPeso(peso)
        self.vertices[id].setCoordenadas(x, y)

    def _print_(self):
        # print(self.vertices)
        print(self.arestas)
    

    @classmethod
    def all(cls):
        return cls.objects

    



g = Grafo()
g.addVertices(5)
g.addAresta([(1,2), (2,1)])
g._print_()
