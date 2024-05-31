#SERVIDOR
import socket
import json
from componentes import sensor

#aceitar conexoes - ok
#receber leitura dos sensores
#ligar e desligar atuadores

#alguma coisa que possa alterar a numeração e poder enviar pros atuadores e sensores os cod de conexao atuais

class gerenciador:
   def __init__(self, codConexao):
      self.atuadores = {}
      self.sensores = {}
      self.clientes = {}
      self.parametros = {} #max e min -> autor do sensor
      self.codConexao = codConexao 
      

   def server (self, host = 'localhost', port=5000):
      self.socketGenrenciador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socketGenrenciador.bind((host, port)) #Define a porta do servidor para que os clientes se conectem
      self.socketGenrenciador.listen() #espera um sinal do cliente 

      print ('Aguardando conexão de um cliente...')

      conexao, ender = self.socketGenrenciador.accept()
      mensagem_inicial = json.loads(conexao.recv(1025).decode('utf-8'))
                  
      print (f'Conexão estabelecida com {mensagem_inicial['autor']}-{mensagem_inicial['id']}')
      
      # condição de aceitação
      if mensagem_inicial['codigo_conexao'] == self.codConexao:
         resposta = {'status': True}
         conexao.sendall(json.dumps(resposta).encode('utf-8'))
         if mensagem_inicial['tipo'] == 'Sensor':
            self.sensores[f"{mensagem_inicial['autor']}"] = [None, conexao]
            self.parametros[f"{mensagem_inicial['autor']}"] = [20,80]
         elif mensagem_inicial['tipo'] == 'Atuador':
            self.atuadores[f"{mensagem_inicial['autor']}"] = None
         else:
            self.clientes[f"{mensagem_inicial['autor']}"] = None
      else:
         resposta = {'status': False}
         conexao.sendall(json.dumps(resposta).encode('utf-8'))
         conexao.close()

      if resposta['status'] == True:
         while True:   
            #tudo que pode receber de mensagens
            dados = conexao.recv(1024).decode()
            mensagem = json.loads(dados)

            if(mensagem["tipo"] == "Sensor"):
               self.sensores[f'{mensagem["autor"]}'] = mensagem['valor']
               sensorParam = self.parametros[f'{mensagem["autor"]}']
               if mensagem['valor'] < sensorParam[0]:
                  #aquecedor
                  #irrigação
                  #injetor

               
               self.LigaDesliga(mensagem)
            elif(mensagem['tipo'] == "Atuador"):
               self.atuadores[f'{mensagem["autor"]}'] = mensagem['status']
            elif(mensagem["tipo"] == "Cliente"):
               self.EnviarUltimaLeitura(mensagem, conexao)

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