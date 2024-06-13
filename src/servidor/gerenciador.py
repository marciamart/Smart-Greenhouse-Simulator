import socket
import json
import threading

class Gerenciador:
    def __init__(self, codConexao):
        self.atuadores = {}
        self.sensores = {}
        self.clientes = {}
        self.parametros = {}  # max e min -> autor do sensor
        self.acao = {
            'temperatura': ['aquecedor', 'resfriador'],
            'umidade': ['irrigacao'],
            'nivelCO2': ['injetor']
        }
        self.codConexao = codConexao

    def server(self, host='localhost', port=5000):
        self.socketGerenciador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketGerenciador.bind((host, port))
        self.socketGerenciador.listen(10)

        print('Aguardando conexão de um cliente...')
        while True:
            conexao, _ = self.socketGerenciador.accept()
            threading.Thread(target=self.conexoes, args=(conexao,)).start()

    def conexoes(self, conexao):
        try:
            data = conexao.recv(1024).decode('utf-8')
            mensagem_inicial = json.loads(data)
            
            print(f"Conexão estabelecida com {mensagem_inicial['autor']}-{mensagem_inicial['id']}")
            
            if mensagem_inicial['codigo_conexao'] == self.codConexao:
                resposta = {'status': True}
                conexao.sendall(json.dumps(resposta).encode('utf-8'))
                if mensagem_inicial['tipo'] == 'Sensor':
                    self.sensores[mensagem_inicial['autor']] = [None, conexao]
                    self.parametros[mensagem_inicial['autor']] = [20, 80]
                elif mensagem_inicial['tipo'] == 'Atuador':
                    self.atuadores[mensagem_inicial['autor']] = [None, conexao]
                else:
                    self.clientes[mensagem_inicial['autor']] = conexao
            else:
                resposta = {'status': False}
                conexao.sendall(json.dumps(resposta).encode('utf-8'))
                conexao.close()
                return

            if resposta['status']:
                while True:
                    data = conexao.recv(1024).decode('utf-8')
                    mensagem = json.loads(data)
                    print(f"Mensagem recebida: {mensagem}")

                    if mensagem["tipo"] == "Sensor":
                        self.sensores[mensagem["autor"]][0] = mensagem['valor']
                        sensorParam = self.parametros.get(mensagem["autor"], [20, 80])
                        atuadores = self.acao.get(mensagem["autor"], [])

                        for atuador in atuadores:
                            if atuador not in self.atuadores:
                                print(f"Atuador {atuador} não encontrado.")
                                continue

                            if mensagem['valor'] < sensorParam[0]:  # Parametro Minimo
                                comando = {'mensagem': 'ligar'}
                                conn = self.atuadores[atuador][1]
                                conn.sendall(json.dumps(comando).encode('utf-8'))
                            elif mensagem['valor'] > sensorParam[1]:  # Parametro Maximo
                                comando = {'mensagem': 'ligar'}
                                if atuador == 'resfriador':
                                    conn = self.atuadores['resfriador'][1]
                                else:
                                    conn = self.atuadores[atuador][1]
                                conn.sendall(json.dumps(comando).encode('utf-8'))
                            else:  # desliga os demais se estiverem acima do max caso esteja ligado
                                comando = {'mensagem': 'desligar'}
                                if self.atuadores[atuador][0]:
                                    conn = self.atuadores[atuador][1]
                                    conn.sendall(json.dumps(comando).encode('utf-8'))

                    elif mensagem["tipo"] == "Atuador":
                        self.atuadores[mensagem["autor"]][0] = mensagem['status']

                    elif mensagem["tipo"] == "Cliente":
                        if mensagem['acao'] == 'valor sensor':
                            valor = self.sensores.get(mensagem['solicitado'], [None, None])[0]
                            resposta = {'valor': valor}
                            conexao.sendall(json.dumps(resposta).encode('utf-8'))

                        elif mensagem['acao'] == 'Atuadores ativos':
                            atuadores_ativos = []
                            for atuador, estado in self.atuadores.items():  # Corrigido aqui
                                if estado[0] == True:
                                    atuadores_ativos.append(atuador)
                            resposta = {'atuadores': atuadores_ativos}
                            conexao.sendall(json.dumps(resposta).encode('utf-8'))

                        elif mensagem['acao'] == 'alterar parametro':
                            self.parametros[mensagem["solicitado"]] = mensagem['parametros']
                            resposta = {'mensagem': 'efetuada com sucesso'}
                            conexao.sendall(json.dumps(resposta).encode('utf-8'))
        except Exception as e:
            print(f"Erro na conexão: {e}")

