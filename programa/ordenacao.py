#Algoritmo separa regiao para robos

vetCapRobot = []
for i in range(robotMap[1]):
    capMinimaAtingida = True
    regioesVisita = []
    #regioesVisita.clear()
    somatorioDemanda = 0
    demanda = 0
    
    while capMinimaAtingida and len(demandaTupla) > demanda:
        if (somatorioDemanda + demandaTupla[demanda][1] <= robotMap[3]):
            somatorioDemanda += demandaTupla[demanda][1]
            regioesVisita.append(demandaTupla[demanda])
            del(demandaTupla[demanda])
            #if(somatorioDemanda >= capMinCaminhao):
                #capMinimaAtingida = False
        demanda += 1
    vetCapRobot.append(regioesVisita)
    
    
print (vetCapRobot)