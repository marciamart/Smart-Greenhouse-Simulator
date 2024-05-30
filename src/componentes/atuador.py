import socket
import json
import time

class Atuador:
    def _init_(self, id):
        self.status = None
        self.id = id

    def ligar(self):
        self.status = True
        print(f"Atuador {self.id} ligado")

    def desligar(self):
        self.status = False
        print(f"Atuador {self.id} desligado")

    def conectarGerenciador(self, host='localhost', port=5000):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client_socket.connect((host, port))
            print(f"Conexão estabelecida em {host}:{port}")

            mensagem_inicial = {"autor": "Atuador", "id": self.id, "codigo_conexao": 00000}
            client_socket.sendall(json.dumps(mensagem_inicial).encode('utf-8'))

            resposta = json.loads(client_socket.recv(1024).decode('utf-8'))

            if resposta.get("status") == "aceito":

                while True:
                    comando = json.loads(client_socket.recv(1024).decode('utf-8'))
                    self.processarComando(comando, client_socket)
            else:
                print("Conexão não aceita pelo gerenciador")
                client_socket.close()

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            client_socket.close()

    def processarComando(self, comando, client_socket):
        if comando.get("comando") == "ligar":
            self.ligar()
        elif comando.get("comando") == "desligar":
            self.desligar()
        else:
            print(f"Comando desconhecido: {comando}")

        
        resposta = {"id": self.id, "status": self.status} # Enviar resposta ao gerenciador confirmando a ação tomada
        client_socket.sendall(json.dumps(resposta).encode('utf-8'))