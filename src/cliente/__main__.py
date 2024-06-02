from cliente import Cliente

def main():
    codConexao = input('insira código de conexão:')
    cliente = Cliente('chefe', codConexao)

    cliente.conectarGerenciador()

if __name__ == "__main__":
    main()