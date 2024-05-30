#SERVIDOR
import socket
import json
from componentes import sensor

#aceitar conexoes
#receber leitura dos sensores
#ligar e desligar atuadores


codConexao = 00000
#alguma coisa que possa alterar a numeração e poder enviar pros atuadores e sensores os cod de conexao atuais

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
      while True:
         conexao, ender = self.socketGenrenciador.accept()
         mensagem_inicial = json.loads(conexao.recv(1025).decode('utf-8'))
                    
         print (f'Conectado em {mensagem_inicial['autor']}-{mensagem_inicial['id']}')
         while True:
            dados = conexao.recv(1024).decode()
            
            if not dados:
               print ('Fechando a conexão')
               conexao.close()
               break

            else:
               mensagem = json.loads(dados)
               if(mensagem["autor"] == "Sensor"):
                  self.ArmazenarUltimaLeitura(mensagem)
                  self.EnviarUltimaLeitura(mensagem, conexao)
               elif(mensagem['autor'] == "Atuador"):
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