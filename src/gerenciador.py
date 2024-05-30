#SERVIDOR
import socket
import json
from componentes import sensor

codConexao = 00000

class gerenciador:
   def __init__(self):
      self.atuadores = []
      self.sensores = [] 
      

   def server (self, host = 'localhost', port=5000):
      self.socketGenrenciador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socketGenrenciador.bind((host, port)) #Define a porta do servidor para que os clientes se conectem
      self.socketGenrenciador.listen() #espera um sinal do cliente 

      print ('Aguardando conexão de um cliente...')

      # condição de aceitação
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
      valorSensor = float(msg["valor"])
      for sensor in self.sensores:
         if(sensor.id == idSensor):
            sensor.valor = valorSensor


   def EnviarUltimaLeitura(self, msg, conexao):
      idSensor = int(msg["id"])
      for sensor in self.sensores:
         if(sensor.id == idSensor):
            UltimaLeitura = {"autor": "Gerenciador", "id" : sensor.id, "valor" : sensor.valor}
            conexao.sendall(json.dumps(UltimaLeitura).encode('utf-8'))


   def LigaDesliga(self, msg):
      idAtuador = int(msg["id"])
      statusAtuador= bool(msg["valor"])
      for atuador in self.atuadores:
         if(atuador.id == idAtuador):
            if(statusAtuador == False):
               atuador.ligar()
            else:
               atuador.desligar()