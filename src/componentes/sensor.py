import time
import random
import threading
import socket
import json

class Sensor: 
    def __init__(self,tipo, codConex):
        self.id = id(self)
        self.valor = None
        self.tipo = tipo
        self.codConex = codConex
        self.run = True
        threading.Thread(target=self.iniciarLeitura).start()

    #métodos criados para operar as ações relacionadas a leitura dos sensores
    def iniciarLeitura(self):
        while True:
            self.valor = random.triangular(10, 90, 40) #Gera um valor aleatório entre o intervalo definido com uma média entre os parâmetros
    
    def pararLeitura(self):
        self.run = False

    def conectarGerenciador(self, host='localhost', port=5000):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um socket TCP/IP
        
        try:
            self.client_socket.connect((host, port)) # Conecta o socket ao gerenciador no host e porta especificados
            print(f"estabelecido conexão em {host}:{port}")

            #primeira mensagem para aceitação de conexão
            messagem_inicial = {"tipo": "Sensor","autor" : "{self.tipo}", "id": self.id, "codigo_conexao": self.codConex}
            self.client_socket.sendall(json.dumps(messagem_inicial).encode('utf-8'))

            #resposta se foi aceito ou nao
            resposta = json.loads(self.client_socket.recv(1025).decode('utf-8'))
            
            if resposta["status"]==True and self.client_socket:  # Verifica se o socket está conectado
                #enviando leitura de 1 em 1 segundo
                while True:
                    messagem = {"tipo": "Sensor", "autor" : "{self.tipo}", "id": self.id, "valor": self.valor} # Cria a mensagem a ser enviada contendo o ID do sensor e o valor atual
                    self.client_socket.sendall(json.dumps(messagem).encode('utf-8'))
                    time.sleep(1)
            else:
                return resposta

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.client_socket.close()