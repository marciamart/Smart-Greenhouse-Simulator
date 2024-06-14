from atuador import Atuador
from sensor import Sensor
import threading
def main():
    codConexao = input('insira código de conexão:')

    #atuadores
    aquecedor = Atuador('aquecedor', codConexao)
    resfriador = Atuador('resfriador', codConexao)
    irrigacao = Atuador('irrigacao', codConexao)
    injetor = Atuador('injetor', codConexao)
    Atuadores = [aquecedor, resfriador, irrigacao, injetor]

    #cria uma thread para cada atuador que se conectar ao Gerenciador
    for atuador in Atuadores:
        threading.Thread(target=atuador.conectarGerenciador).start()

    #sensores
    temperatura = Sensor('temperatura', codConexao)
    umidade = Sensor('umidade', codConexao)
    nivelCO2 = Sensor('nivelCO2', codConexao)
    sensores = [temperatura, umidade, nivelCO2]
    print('sensores ativados')

    #cria uma thread para cada sensor que se conectar ao Gerenciador
    for sensor in sensores:
        threading.Thread(target=sensor.conectarGerenciador).start()
    
if __name__ == "__main__":
    main()