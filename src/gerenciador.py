#SERVIDOR
import socket
import json
from componentes import sensor

class gerenciador:
   def __init__(self):
      self.atuadores = []
      self.sensores = [] 
      self.socketGenrenciador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

   def server (self, host = 'localhost', port=5000):
      self.socketGenrenciador.bind((host, port))
      self.socketGenrenciador.listen()
      print ('Aguardando conexão de um cliente')
      conexao, ender = self.socketGenrenciador.accept()
      print ('Conectado em', ender)
      while True:
         dados = conexao.recv(1024).decode()
         if not dados:
            print ('Fechando a conexão')
            conexao.close()
            break
         else:
            mensagem = json.loads(dados)
            if(mensagem["quemEnviou"] == "Sensor"):
               self.ArmazenarUltimaLeitura(mensagem)
            elif(mensagem['quemEnviou'] == "Atuador"):
               self.LigaDesliga(mensagem)


   def ArmazenarUltimaLeitura(self, msg):
      idSensor = int(msg["id"])
      valorSensor = int(msg["valor"])
      for sensor in self.sensores:
         if(self.sensores[sensor].id == idSensor):
            self.sensores[sensor].valor = valorSensor


   def EnviarUltimaLeitura(self, msg):
      pass


   def LigaDesliga(self, msg):
      idAtuador = int(msg["id"])
      statusAtudor= bool(msg["valor"])
      for atuador in self.atuadores:
         if(self.atuadores[atuador].id == idAtuador):
            if(statusAtudor == False):
               self.atuadores[atuador].ligar()
            else:
               self.atuadores[atuador].desligar()
   
  