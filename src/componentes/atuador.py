import socket
import json

class Atuador:
    def __init__(self, tipo, codConex):
        self.status = False
        self.id = id(self)
        self.tipo = tipo
        self.codConex = codConex

    #método que muda o estado do atuador (Liga)
    def ligar(self):
        self.status = True
        print(f"Atuador {self.tipo}:{self.id} ligado")

    #método que muda o estado do atuador (Desliga)
    def desligar(self):
        self.status = False
        print(f"Atuador {self.tipo}:{self.id} desligado")

    #método que processa o comando requisitado pelo gerenciador e muda o estado do atuador
    def processarComando(self, comando, client_socket):
        if comando['mensagem'] == "ligar":
            self.ligar()
        elif comando['mensagem'] == "desligar":
            self.desligar()
        else:
            print(f"Comando desconhecido: {comando}")

        #mensagem contendo o estado do atuador após seu estado ser processado pelo Gerenciador
        estado = {"tipo": "Atuador", 
                  "autor": self.tipo, 
                  "id": self.id, 
                  "status": self.status
                  }      
          
        # Enviar resposta ao gerenciador confirmando a ação tomada
        client_socket.sendall(json.dumps(estado).encode('utf-8'))

    def conectarGerenciador(self, host='localhost', port=5000):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client_socket.connect((host, port))
            print(f"{self.tipo} estabeleceu conexão em {host}:{port}")

            #mensagem de requisição de conexão
            mensagem_inicial = {"tipo": "Atuador",
                                "autor":self.tipo, 
                                "id": self.id, 
                                "codigo_conexao":  self.codConex}
            
            client_socket.sendall(json.dumps(mensagem_inicial).encode('utf-8'))
            
            data = client_socket.recv(1024).decode('utf-8')
            resposta = json.loads(data) 

            #resposta se foi aceito ou não
            print(resposta)

            if resposta["status"] == True: #Caso a conexão seja positiva, processará um comando requisitado pelo Gerenciador
                while True:
                    comando = json.loads(client_socket.recv(1024).decode('utf-8'))
                    self.processarComando(comando, client_socket)
            else: #Em caso negativo, a conexão é interrompida
                print("Conexão não aceita pelo gerenciador")
                client_socket.close()

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            client_socket.close()