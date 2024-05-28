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