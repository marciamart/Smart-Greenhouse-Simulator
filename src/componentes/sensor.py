import time #módulo para funções relacionadas ao tempo 
import random #módulo para gerar números aleatrórios 
import threading #módulo que permite a execução de várias operações ao mesmo tempo
import socket
class sensor: 
    def _init_(self, paramMin, paramMax):
        self.id = id(self)
        self.valor = None
        self.paramMin = paramMin
        self.paramMax = paramMax
        self.run = True

    threading.Thread(target=self.iniciarLeitura).start()

    #métodos criados para operar as ações relacionadas a leitura dos sensores
    def iniciarLeitura(self):
        while True:
            self.valor = random.triangular(self.paramMin, self.paramMax, (self.paramMax+self.paramMin)/2) #Gera um valor aleatório entre o intervalo definido com uma média entre os parâmetros
    
    def pararLeitura(self):
        self.run = False

    def getValor(self):
        return self.valor

    def conectarGerenciador(self, host = 'localhost', port = 5000):
        self.client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host,port))
        