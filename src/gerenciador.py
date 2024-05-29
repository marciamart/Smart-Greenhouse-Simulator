#SERVIDOR
import socket

class gerenciador:
   def __init__(self):
      self.conexoes = [[]]

   def server (host = 'localhost', port=5000):

      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.bind((host, port))
      s.listen()
      print ('Aguardando conexão de um cliente')
      conn, ender = s.accept()
      print ('Conectado em', ender)
      while True:
         data = conn.recv(1024)
         if not data:
            print ('Fechando a conexão')
            conn.close()
            break
         conn.sendall(data)

   def ArmazenarUltimaLeitura():
      pass

   def LigaDesliga():
      pass
   
   def ultimaLeitura():
      pass