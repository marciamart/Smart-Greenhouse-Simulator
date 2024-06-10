from gerenciador import Gerenciador
import threading

def main():
    codConexao = input('insira código de conexão:')

    gerenciador = Gerenciador(codConexao)
    gerenciador.server()
    
if __name__ == "__main__":
    main()