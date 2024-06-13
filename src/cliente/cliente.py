import socket
import json

class Cliente:
    def __init__(self, tipo, codConex):
        self.id = id(self)
        self.tipo = tipo
        self.codConex = codConex

    def conectarGerenciador(self, host='localhost', port=5000):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.client_socket.connect((host, port))
            print(f"Conexão estabelecida em {host}:{port}")

            mensagem_inicial = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, "codigo_conexao": self.codConex}
            self.client_socket.sendall(json.dumps(mensagem_inicial).encode('utf-8'))
            print('Esperando autorização...')

            resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
            if resposta["status"]:
                print('Autorização concedida')
                self.menu()
            else:
                print("Conexão não aceita pelo gerenciador")
                self.client_socket.close()

        except Exception as e:
            print(f"Erro ao conectar: {e}")
            self.client_socket.close()

    def menu(self):
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
                opc = input("\nEscolha uma opção: ")

                if opc == 'a':
                    sensor = 'temperatura'
                elif opc == 'b':
                    sensor = 'umidade'
                elif opc == 'c':
                    sensor = 'nivelCO2'
                else:
                    print("Opção inválida, por favor, escolha uma opção entre 'a' e 'c'.")
                    continue
                
                mensagem = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, 'acao': 'valor sensor', "solicitado": sensor}
                self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
                print(f"Valor do sensor {sensor}: {resposta['valor']}")

            elif escolha == '2':
                mensagem = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, 'acao': 'Atuadores ativos'}
                self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
                atuadores_ativos = resposta['atuadores']
                print('Atuadores ativos:')
                for atuador in atuadores_ativos:
                    print(atuador)

            elif escolha == '3':
                print('Escolha qual parâmetro deseja alterar:')
                print("a. Temperatura")
                print("b. Umidade do solo")
                print("c. Nivel de CO2")

                opc = input("\nEscolha uma opção: ")
                if opc == 'a':
                    sensor = 'temperatura'
                elif opc == 'b':
                    sensor = 'umidade'
                elif opc == 'c':
                    sensor = 'nivelCO2'
                else:
                    print("Opção inválida, por favor, escolha uma opção entre 'a' e 'c'.")
                    continue

                print(f'Alterando parâmetros do sensor: {sensor}')
                paramMin = input('Parâmetro Mínimo: ')
                paramMax = input('Parâmetro Máximo: ')
                
                mensagem = {"tipo": "Cliente", "autor": self.tipo, "id": self.id, 'acao': 'alterar parametro', "solicitado": sensor, 'parametros': [paramMin, paramMax]}
                self.client_socket.sendall(json.dumps(mensagem).encode('utf-8'))

                resposta = json.loads(self.client_socket.recv(1024).decode('utf-8'))
                print(f"Alteração {resposta['mensagem']}")

            elif escolha == '4':
                print("Saindo do menu. Até logo!")
                break
            else:
                print("Opção inválida, por favor, escolha uma opção de 1 a 4.")

# Exemplo de uso
if __name__ == "__main__":
    cliente = Cliente(tipo="chefe", codConex="12345")
    cliente.conectarGerenciador()
