import socket
import json

class Cliente:
    def __init__(self, tipo, codConex):
        self.id = id(self)  # Gera um ID único para o cliente
        self.tipo = tipo  # Define o tipo do cliente
        self.codConex = codConex  # Código de conexão para autenticação

    def conectarGerenciador(self, host='localhost', port=5000):
        # Método para conectar ao gerenciador
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Cria um socket TCP/IP
        try:
            self.client_socket.connect((host, port))  # Conecta ao gerenciador
            print(f"Conexão estabelecida em {host}:{port}")

            # Envia uma mensagem inicial para o gerenciador
            mensagem_inicial = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, "codigo_conexao": self.codConex}
            self.client_socket.sendall(json.dumps(mensagem_inicial).encode('utf-8'))
            print('Esperando autorização...')

            # Recebe a resposta do gerenciador
            resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
            if resposta["status"]:
                print('Autorização concedida')
                self.menu()  # Inicia o menu de opções se a conexão for aceita
            else:
                print("Conexão não aceita pelo gerenciador")
                self.client_socket.close()
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.client_socket.close()

    def menu(self):
        # Menu principal de opções para o cliente
        while True:
            print("\nEscolha uma opção: ")
            print("[1] Leitura dos sensores")
            print("[2] Atuadores em funcionamento")
            print("[3] Parâmetros na estufa")
            print("[4] Sair")

            escolha = input('\nEscolha uma opção: ')

            if escolha == '1':
                # Menu para leitura dos sensores
                while True:
                    print("\nQual sensor deseja ter a leitura?")
                    print("a. Temperatura")
                    print("b. Umidade do solo")
                    print("c. Nivel de CO2")
                    print("d. Voltar")
                    opc = input("\nEscolha uma opção: ")

                    if opc == 'a':
                        sensor = 'temperatura'
                    elif opc == 'b':
                        sensor = 'umidade'
                    elif opc == 'c':
                        sensor = 'nivelCO2'
                    elif opc == 'd':
                        break  
                    else:
                        print("Opção inválida, por favor, escolha uma opção entre 'a' e 'd'.")
                        continue

                    # Envia solicitação para obter o valor do sensor selecionado
                    mensagem = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, 'acao': 'valor sensor', "solicitado": sensor}
                    self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))
                    resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))

                    # Exibe o valor do sensor
                    if sensor == 'temperatura':
                        print(f"\nValor do sensor {sensor}: {resposta['valor']:.2f}ºC")
                    else:
                        print(f"\nValor do sensor {sensor}: {resposta['valor']:.2f}%")
                        
            elif escolha == '2':
                # Solicita a lista de atuadores ativos
                mensagem = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, 'acao': 'Atuadores ativos'}
                self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
                atuadores_ativos = resposta['atuadores']
                if atuadores_ativos != 'Nenhum atuador ativo':
                    print('\nAtuadores ativos:\n')
                    for atuador in atuadores_ativos:
                        print(atuador)
                else:
                    print(atuadores_ativos)

            elif escolha == '3':
                # Menu para alterar parâmetros dos sensores
                while True:
                    print('\nEscolha qual parâmetro deseja alterar:')
                    print("a. Temperatura")
                    print("b. Umidade do solo")
                    print("c. Nivel de CO2")
                    print("d. Voltar")

                    opc = input("\nEscolha uma opção: ")
                    if opc == 'a':
                        sensor = 'temperatura'
                    elif opc == 'b':
                        sensor = 'umidade'
                    elif opc == 'c':
                        sensor = 'nivelCO2'
                    elif opc == 'd':
                        break  # Volta ao menu principal
                    else:
                        print("\nOpção inválida, por favor, escolha uma opção entre 'a' e 'd'.")
                        continue

                    print(f'\nAlterando parâmetros do sensor: {sensor}')
                    paramMin = input('Parâmetro Mínimo: ')
                    paramMax = input('Parâmetro Máximo: ')
                    print('\nProcessando...')
                    
                    # Envia solicitação para alterar os parâmetros do sensor selecionado
                    mensagem = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, 'acao': 'alterar parametro', "solicitado": sensor, 'parametros': [paramMin, paramMax]}
                    self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                    resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
                    print(f"\nAlteração {resposta['mensagem']}")

            elif escolha == '4':
                # Sai do menu
                print("\nSaindo do menu. Até logo!")
                break
            else:
                print("Opção inválida, por favor, escolha uma opção de 1 a 4.")
