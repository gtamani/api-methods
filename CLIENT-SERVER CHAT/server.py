import socket,threading,sys, pickle,os


class Server():

    def __init__(self, host="localhost",port=8000):
        self.connected_clients = []
        self.listening = 0
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((host,port))
        self.server.listen(5)
        self.server.setblocking(False)

        #Create daemon threads.
        accept = threading.Thread(target=self.accept)
        process = threading.Thread(target=self.process)
        accept.daemon, process.daemon = True, True
        accept.start()
        process.start()

        os.system("cls")
        print("--- SERVER ---")

        while 1:
            
            msg = input("")
            if msg == "q":
                sys.exit()
            

    def accept(self):
        while 1:
            try:
                conn, addr = self.server.accept()
                conn.setblocking(False)
                self.connected_clients.append(conn)
            except:
                pass          
            
    def process(self):
        while 1:

            if len(self.connected_clients) != self.listening:
                self.listening = len(self.connected_clients)
                print(self.listening," usuarios conectados!")

            if len(self.connected_clients) > 0:
                for client in self.connected_clients:
                    try:
                        data = client.recv(1024)
                        if data:
                            self.message_to_all(data,client)
                    except:
                        pass
    
    def message_to_all(self,data,client):
        print("Mensaje enviado!")
        for cl in self.connected_clients:
            if client != cl:
                cl.send(data)
        


server = Server()