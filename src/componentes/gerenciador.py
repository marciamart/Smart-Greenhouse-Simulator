#SERVIDOR
import socket
import json
from componentes import sensor

#aceitar conexoes - ok
#receber leitura dos sensores
#ligar e desligar atuadores

#alguma coisa que possa alterar a numeração e poder enviar pros atuadores e sensores os cod de conexao atuais

class Gerenciador:
   def __init__(self, codConexao):
      self.atuadores = {}
      self.sensores = {}
      self.clientes = {}
      self.parametros = {} #max e min -> autor do sensor
      self.acao = {
         'temperatura': ['aquecedor','resfriador'],
         'umidade': 'irrigacao',
         'nivelCO2': 'injetor'
      }
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
            self.atuadores[f"{mensagem_inicial['autor']}"] = [None, conexao]
         else:
            self.clientes[f"{mensagem_inicial['autor']}"] =  conexao
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
               self.sensores[f'{mensagem["autor"]}'][0] = mensagem['valor']
               sensorParam = self.parametros[f'{mensagem["autor"]}']
               atuador = self.acao[f'{mensagem["autor"]}'][0] 
               #         x                 min       
               if mensagem['valor'] < sensorParam[0]: #Parametro Minimo
                  comando = {'mensagem': 'ligar'}
                  #encontra conexao(conn) do seu atuador 
                  conn = self.atuadores[atuador][1]
                  conn.sendall(json.dumps(comando).encode('utf-8'))
               elif mensagem['valor'] > sensorParam[1]: #Parametro Maximo
                  if mensagem["autor"] == 'temperatura':
                     comando = {'mensagem': 'ligar'}
                     conn = self.atuadores['resfriador'][1]
                     conn.sendall(json.dumps(comando).encode('utf-8'))
               else: # desliga os demais se estiverem acima do max caso esteja ligado
                  comando = {'mensagem': 'desligar'}
                  if atuador[0] == True:
                     conn = self.atuadores[atuador][1]
                     conn.sendall(json.dumps(comando).encode('utf-8'))

            elif(mensagem['tipo'] == "Atuador"):
               self.atuaores[f'{mensagem["autor"]}'] = mensagem['status']

            elif(mensagem["tipo"] == "Cliente"):
               if mensagem['acao'] == 'valor sensor': #quer pegar o valor do sensor 
                  valor = self.sensores[mensagem['solicitado']][0]
                  resposta = {'valor': valor}
                  conexao.sendall(json.dumps(resposta).encode('utf-8'))

               elif mensagem['acao'] == 'Atuadores ativos':
                  atuadores_ativos = []
                  for atuador, bole in self.atuadores.items():
                     if bole[0]  == True:
                        atuadores_ativos.append(atuador)
                  resposta = {'atuadores': atuadores_ativos}
                  conexao.sendall(json.dumps(resposta).encode('utf-8'))

               elif mensagem['acao'] == 'alterar parametro':
                  self.parametros[f'{mensagem['solicitado']}'] = mensagem['parametros']
                  resposta = {'mensagem': 'efetuada com sucesso'}
                  conexao.sendall(json.dumps(resposta).encode('utf-8'))