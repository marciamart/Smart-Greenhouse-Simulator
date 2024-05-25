class Atuador:
    def __init__(self, onOff, id):
        self.onOff = onOff
        self.id = id
        
    def ligar(self, ligar):
        if(ligar == True and self.onOff == False):
            self.onOff = True
        else:
            pass
    
    def Desligar(self, Desligar):
        if(Desligar == True and self.onOff == True):
            self.onOff = True
        else:
            pass
            
            
        
Aquecedor = Atuador(False, 1)
resfriador = Atuador(False, 2)
irrigador = Atuador(False, 3)
injetorCo2 = Atuador(False, 4)

