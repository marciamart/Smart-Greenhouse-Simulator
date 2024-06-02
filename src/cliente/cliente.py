import socket
import json

class Cliente:
    def __init__(self,tipo, codConex):
        self.id = id(self)
        self.tipo = tipo
        self.codConex = codConex
        

    def conectarGerenciador(self, host='localhost', port=5000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect((host, port))
            print(f"estabelecido conexão em {host}:{port}")

            mensagem_inicial = {"tipo": "Cliente","autor":self.tipo, "id": self.id, "codigo_conexao":  self.codConex}
            self.client_socket.sendall(json.dumps(mensagem_inicial).encode('utf-8'))
            print('em espera de autorizacao...')

            resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
            print('aguardando...')
            if resposta["status"] == True:
                print('autorizacao concedida')
                self.menu()
            else:
                print("Conexão não aceita pelo gerenciador")
                self.client_socket.close()

        except Exception as e:
                print(f"Erro ao conectar: {e}")
                self.client_socket.close()

    def menu(self):
        print('jbrbgrb')
        while True:
            print("\nEscolha uma opção: ")
            print("[1] Leitura dos sensores")
            print("[2] Atuadores em funcionamento")
            print("[3] Parâmetros na estufa")
            print("[4] Sair")
        
            escolha = input()

            if escolha == '1':
                
                print("\nQual sensor deseja ter a leitura?")
                print("a. Temperatura")
                print("b. Umidade do solo")
                print("c. Nivel de CO2")
                opc = input("\nEscolha uma opção:\n")
                # Chame uma função ou adicione a lógica para a Opção 1 aqui
                if opc == 'a':
                    sensor = 'temperatura'
                elif opc == 'b':
                    sensor = 'umidade'
                elif opc == 'c':
                    sensor = 'nivelCO2'
                else:
                    print("Opção inválida, por favor, escolha uma opção entre 'a' e 'c'.")
                
                mensagem = {"tipo": "Cliente","autor":f"{self.tipo}", "id": self.id,'acao': 'valor sensor', "solicitado":  f'{sensor}'}
                self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
                print(resposta['valor'])

            elif escolha == '2':
                print("Você escolheu a Opção 2.")
                # Chame uma função ou adicione a lógica para a Opção 2 aqui
                mensagem = {"tipo": "Cliente","autor":f"{self.tipo}", "id": self.id, 'acao':'Atuadores ativos',"solicitato": 'Atuadores ativos'}
                self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))

                print('Aqui estão seus atuadores ativos:\n')
                atuador = resposta['atuadores']
                for i in atuador :
                    print(f'{i}\n')

            elif escolha == '3':
                print("Você escolheu a Opção 3.")
                # Chame uma função ou adicione a lógica para a Opção 3 aqui
                print('Escolha qual parâmetro deseja alterar:')
                print("a. Temperatura")
                print("b. Umidade do solo")
                print("c. Nivel de CO2")

                opc = input("\nEscolha uma opção:\n")
                if opc == 'a':
                    sensor = 'temperatura'
                elif opc == 'b':
                    sensor = 'umidade'
                elif opc == 'c':
                    sensor = 'nivelCO2'
                else:
                    print("Opção inválida, por favor, escolha uma opção entre 'a' e 'c'.")

                print(f'Você solicitou a alteração do parâmetro do sensor:{sensor}')
                paramMin = input('Parâmetro Mínimo: ')
                paramMax = input('Parâmetro Máximo: ')
                
                mensagem = {"tipo": "Cliente","autor":f"{self.tipo}", "id": self.id,'acao':'alterar parametro', "solicitado":  f'{sensor}', 'parametros': [paramMin, paramMax]}
                self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))

                print(f'Sua alteração foi {resposta[mensagem]}!')

            elif escolha == '4':
                print("Saindo do menu. Até logo!")
                break
            else:
                print("Opção inválida, por favor, escolha uma opção de 1 a 4.")

