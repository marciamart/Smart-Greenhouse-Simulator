import socket
import json

class Atuador:
    def __init__(self, tipo, codConex):
        self.status = None
        self.id = id(self)
        self.tipo = tipo
        self.codConex = codConex

    def ligar(self):
        self.status = True
        print(f"Atuador {self.tipo}:{self.id} ligado")

    def desligar(self):
        self.status = False
        print(f"Atuador {self.tipo}:{self.id} desligado")

    def processarComando(self, comando, client_socket):
        if comando['mensagem'] == "ligar":
            self.ligar()
        elif comando['mensagem'] == "desligar":
            self.desligar()
        else:
            print(f"Comando desconhecido: {comando}")

        estado = {"tipo": "Atuador", "autor": "{self.tipo}", "id": self.id, "status": self.status} # Enviar resposta ao gerenciador confirmando a ação tomada
        client_socket.sendall(json.dumps(estado).encode('utf-8'))

    def conectarGerenciador(self, host='localhost', port=5000):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client_socket.connect((host, port))
            print(f"estabelecido conexão em {host}:{port}")

            mensagem_inicial = {"tipo": "Atuador","autor":{self.tipo}, "id": self.id, "codigo_conexao":  self.codConex}
            client_socket.sendall(json.dumps(mensagem_inicial).encode('utf-8'))

            resposta = json.loads(client_socket.recv(1024).decode('utf-8'))

            if resposta["status"] == True:

                while True:
                    comando = json.loads(client_socket.recv(1024).decode('utf-8'))
                    self.processarComando(comando, client_socket)
            else:
                print("Conexão não aceita pelo gerenciador")
                client_socket.close()

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            client_socket.close()