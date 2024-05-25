import socket

HOST  = 'localhost'
PORT  = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()
print ('Aguardando conexão de um cliente')
conn, ender = s.accept()
print ('Conectado em', ender)
while True:
   data = conn.recv(1024)
   if not data:
      print ('Fechando a conexão')
      conn.close()
      break
   conn.sendall(data)

# nogduda ---------------------------------------------------------------------

import socket
import threading
import time

import random

global temperatura_interna 
global umidade_do_solo
global nivel_de_co2


def sensor_temperatura():
    lista_temperatura = []
    while True:
            lista_temperatura = random.triangular(16, 22, 19)  
            print(f"Temperatura interna: {lista_temperatura:.2f}°C") 
            time.sleep(1) 
            

def sensor_umidade():
    while True:
            umidade_do_solo = random.triangular(50, 80, 70)  
            print(f"Umidade do solo: {umidade_do_solo:.2f}%") 
            time.sleep(1) 

def sensor_co2():
    while True:
            nivel_de_co2 = random.triangular(1200, 1500,1400)  
            print(f"Umidade do solo: {nivel_de_co2:.2f} ppm") 
            time.sleep(1) 

#criando os atuadores
def aquecedor():
    if temperatura_interna < 17:
        print("Iniciando aquecedor...")
    else:
        pass

def resfriador():
    if temperatura_interna > 20:
        print("Iniciando o resfriador...")
    else: 
        pass

def irrigador():
    if umidade_do_solo < 60:
        print("Iniciando o irrigador...")
    else:
        pass

def injetor():
    if nivel_de_co2 < 1300:
        print("Iniciando o injetor de CO2...")
    else: 
        pass

def handle_client(client_socket, client_address):
    """
    Função para lidar com a comunicação com um cliente conectado.
    """
    print(f"Conexão aceita de {client_address}")  # Informa que uma conexão foi estabelecida com o cliente
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')  # Recebe a mensagem do cliente
            if message:
                print(f"Recebido de {client_address}: {message}")  # Exibe a mensagem recebida do cliente
                # Aqui você pode adicionar lógica para responder ou encaminhar a mensagem
            else:
                break  # Se a mensagem estiver vazia, encerra a conexão
        except:
            break  # Em caso de exceção (por exemplo, cliente desconectado), encerra a conexão
    client_socket.close()  # Fecha o socket do cliente

def start_server(host='127.0.0.', port=5555):
    """
    Função para iniciar o servidor.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP
    server.bind((host, port))  # Associa o socket ao endereço e porta especificados
    server.listen(5)  # Habilita o servidor a aceitar conexões, com uma fila máxima de 5 conexões
    print(f"Servidor iniciado em {host}: {port}")  # Informa que o servidor foi iniciado

    while True:
        client_socket, client_address = server.accept()  # Aguarda e aceita uma nova conexão
        # Cria uma nova thread para lidar com o cliente conectado
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()  # Inicia a thread para lidar com o cliente

#if __name__ == "__main__":
    start_server()  # Inicia o servidor se este arquivo for executado como o script principal


def menu():
    while True:
        print("\nEscolha uma opção: ")
        print("1. Leitura dos sensores")
        print("2. Atuadores em funcionamento")
        print("3. Opção 3")
        print("4. Sair")
    
        choice = input("Escolha uma opção (1-4): ")

        if choice == '1':
            
            print("\nQual sensor deseja acessar?")
            print("a. Temperatura")
            print("b. Umidade do solo")
            print("c. Nivel de CO2")
            op= input("\nEscolha uma opção:\n")
            if op == 'a':
                sensor_temperatura()
            
            # Chame uma função ou adicione a lógica para a Opção 1 aqui
        elif choice == '2':
            print("Você escolheu a Opção 2.")
            # Chame uma função ou adicione a lógica para a Opção 2 aqui
        elif choice == '3':
            print("Você escolheu a Opção 3.")
            # Chame uma função ou adicione a lógica para a Opção 3 aqui
        elif choice == '4':
            print("Saindo do menu. Até logo!")
            break
        else:
            print("Opção inválida, por favor, escolha uma opção de 1 a 4.")

menu()