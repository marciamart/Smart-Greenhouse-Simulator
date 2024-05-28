class Atuador:
    def __init__(self, id):
        self.status = None
        self.id = id
        
    def ligar(self):
        self.status = True
        
    def Desligar(self):
        self.status = False

    def conectarGerenciador(self):# mensagens
        pass