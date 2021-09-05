# simple echo server

import socket
import threading

PORT = 5200

class Server():

    def __init__(self, host, port):

        # server address
        self.host = host
        self.port = port

        # create socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # IPv4, TCP

        # socket option to reuse idle socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to address
        self.socket.bind((self.host, self.port))


    def listen(self):

        # start listening for client connections
        self.socket.listen(100)
            # max 100 pending connections

        print('server listening..\n')

        while True:

            # accept new client connection
            client, address = self.socket.accept()

            print('client accepted\n')

            # handle client in separate thread
            handler_thread = threading.Thread(target=self.client_handler, args=(client,))
            handler_thread.start()

    
    def client_handler(self, client):

        recv_size = 1024

        while True:

            try:
                # recieve data from user
                data = client.recv(recv_size)
                print(f'received: {data}')

                if data:
                    # data is received
                    response = data
                    client.send(response)
                        # echo back
                else:
                    raise error('disconnected')

            except:
                # close the socket
                client.close()


# if run as script
if __name__ == "__main__":
    server = Server('', PORT)
    server.listen()
