from atuador import Atuador
from sensor import Sensor

def main():
    codConexao = input('insira código de conexão:')

    #atuadores
    aquecedor = Atuador('aquecedor', codConexao)
    resfriador = Atuador('resfriador', codConexao)
    irrigacao = Atuador('irrigacao', codConexao)
    injetor = Atuador('injetor', codConexao)

    #estabelecendo conexao atuador - gerenciador
    aquecedor.conectarGerenciador()
    resfriador.conectarGerenciador()
    irrigacao.conectarGerenciador()
    injetor.conectarGerenciador()

    #sensores
    temperatura = Sensor('temperatura', codConexao)
    umidade = Sensor('umidade', codConexao)
    nivelCO2 = Sensor('nivelCO2', codConexao)
    print('sensores ativados')
    
    #estabelecendo conexao sensor - gerenciador
    temperatura.conectarGerenciador()
    umidade.conectarGerenciador()
    nivelCO2.conectarGerenciador()

if __name__ == "__main__":
    main()