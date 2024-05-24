import socket

HOST = '127.0.0.1'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(str.encode('Bom dia'))
data = s.recv(1024)
print('Mensagem ecoada:', data.decode())


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