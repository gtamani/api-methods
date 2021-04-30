import socket,threading,sys, pickle,os

class Client():

    def __init__(self, host = "localhost",port=8000):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((host,port))
        self.name = str(input("Welcome to the room, What's your name "))
        
        os.system("cls")
        print("--- "+self.name+" ---\n\n")

        recv = threading.Thread(target=self.recieve)
        recv.daemon = True
        recv.start()

        while 1:
            message = input("")
            if message != "q":
                self.send_msg(message)
            else:
                self.socket.close()
                sys.exit()
        print()


    def recieve(self):
        while 1:
            try:
                data = self.socket.recv(1024)
                if data:
                    data = pickle.loads(data)
                    data = data.split("%&/(")
                    print("{} - ({})".format(data[1],data[0])) #decode()
            except:
                print("\n Chat desconectado, vuelva pronto!")
                sys.exit()
                

    def send_msg(self, message):
        code = self.name+"%&/("+message
        self.socket.send(pickle.dumps(code))  #encode()


client = Client()
