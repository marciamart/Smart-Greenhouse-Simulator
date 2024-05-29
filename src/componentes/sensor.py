import time #módulo para funções relacionadas ao tempo 
import random #módulo para gerar números aleatrórios 
import threading #módulo que permite a execução de várias operações ao mesmo tempo
import socket
class Sensor: 
    def __init__(self, paramMin, paramMax):
        self.id = id(self)
        self.valor = None
        self.paramMin = paramMin
        self.paramMax = paramMax
        self.run = True

    #threading.Thread(target=self.iniciarLeitura).start()

    #métodos criados para operar as ações relacionadas a leitura dos sensores
    def iniciarLeitura(self):
        while True:
            self.valor = random.triangular(self.paramMin, self.paramMax, (self.paramMax+self.paramMin)/2) #Gera um valor aleatório entre o intervalo definido com uma média entre os parâmetros
    
    def pararLeitura(self):
        self.run = False

    def getValor(self):
        return self.valor

    def conectarGerenciador(self, host='localhost', port=5000):
        # Cria um socket TCP/IP
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta o socket ao gerenciador no host e porta especificados
        self.client_socket.connect((host, port))
        print(f"Conectado ao gerenciador em {host}:{port}")

    # Método para enviar a leitura do sensor ao gerenciador
    def enviarLeitura(self):
        try:
            if self.client_socket:  # Verifica se o socket está conectado
                # Cria a mensagem a ser enviada contendo o ID do sensor e o valor atual
                message = {"quemEnviou" : "Sensor", "id": self.id, "valor": self.getValor()}
                print(f"Enviando: {message}")
                # Envia a mensagem ao gerenciador
                self.client_socket.sendall(message.encode('utf-8'))
                # Recebe a resposta do servidor (opcional)
                data = self.client_socket.recv(1024)
                print(f"Recebido do gerenciador: {data.decode('utf-8')}")
        except socket.error as e:  # Captura erros de socket
            print(f"Erro de socket: {e}")
        except Exception as e:  # Captura outras exceções
            print(f"Outra exceção: {e}")

    # Método para desconectar do gerenciador
    def desconectarGerenciador(self):
        if self.client_socket:  # Verifica se o socket está conectado
            self.client_socket.close()  # Fecha a conexão
            print("Desconectado do gerenciador")


# Exemplo de uso
sensor1 = Sensor(10, 50)  # Cria uma instância do sensor com valores mínimos e máximos
sensor1.conectarGerenciador()  # Conecta ao gerenciador

# Simula o envio de leituras ao gerenciador a cada 5 segundos
try:
    while True:
        sensor1.enviarLeitura()  # Envia a leitura atual do sensor
        time.sleep(5)  # Aguarda 5 segundos antes de enviar a próxima leitura
except KeyboardInterrupt:  # Permite interrupção pelo usuário (por exemplo, pressionando Ctrl+C)
    print("Interrompido pelo usuário")
finally:
    sensor1.pararLeitura()  # Para a leitura do sensor
    sensor1.desconectarGerenciador()  # Desconecta do gerenciador