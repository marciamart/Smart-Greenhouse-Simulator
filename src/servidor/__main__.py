from gerenciador import Gerenciador

def main():
    codConexao = input('insira código de conexão:')

    gerenciador = Gerenciador(codConexao)
    gerenciador.server()

if __name__ == "__main__":
    main()