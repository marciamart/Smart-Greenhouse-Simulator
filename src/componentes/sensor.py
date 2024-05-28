import time
import random
import threading

class sensor:
    def _init_(self, paramMin, paramMax):
        self.id = id(self)
        self.valor = None
        self.paramMin = paramMin
        self.paramMax = paramMax
        self.run = True

    threading.Thread(target=self.iniciarLeitura).start()

    def iniciarLeitura(self):
        while True:
            self.valor = random.triangular(self.paramMin, self.paramMax, (self.paramMax+self.paramMin)/2)

    def pararLeitura(self):
        self.run = False

    def getValor(self):
        return self.valor

    def conectarGerenciador(self):# mensagens
        pass