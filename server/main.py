# simple echo server

import socket
import threading

PORT = 5200


rooms = []

class Room():

    def __init__(self, title, tags, goals):
        self.title = title
        self.tags = tags
        self.goals = goals
        self.followers = set()
        self.chat = ''

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

        def can_read():

            decoded_buffer = buffer.decode()

            pos = decoded_buffer.find('\n')
            if pos == -1:
                return False

            size = int(decoded_buffer[:pos].split()[1])

            if len(decoded_buffer) - (pos+1) >= size:
                return True
            return False

        def read():

            nonlocal buffer

            decoded_buffer = buffer.decode()

            pos = decoded_buffer.find('\n')
            size = int(decoded_buffer[:pos].split()[1])

            message = decoded_buffer[pos+1:size+(pos+1)]
            buffer = decoded_buffer[size+(pos+1):].encode()

            handle_message(message)

        def handle_message(message):
            
            pos = message.find('\n')
            if pos == -1:
                pass

            type = message[:pos].split()[1]
            message = message[pos+1:]

            if type == 'username':
                nonlocal client_username
                client_username = message.split()[1]

            elif type == 'create':
                parts = message.split('\n')
                
                title = parts[0][parts[0].find(':')+1:].strip()
                tags = parts[1][parts[1].find(':')+1:].strip()
                goals = parts[2][parts[2].find(':')+1:].strip()

                room = Room(title, tags, goals)
                room.followers.add(client_username)
                room.chat = '--> Discuss about the book here\n'

                rooms.append(room)

            elif type == 'rooms':

                load = ''

                for room in rooms:
                    load += room.title
                    load += '\n'
                    load += room.tags
                    load += '\n'
                    load += room.goals
                    load += '\n'
                    load += 'yes' if client_username in room.followers else 'no'
                    load += '\n'

                client.send((f'size: {len(load)}\n' + load).encode())

            elif type == 'read':
                room_number = int(message.split()[1])

                load = rooms[room_number].chat

                client.send((f'size: {len(load)}\n' + load).encode())

            elif type == 'send':
                pos = message.find('\n')
                room_number = int(message[:pos].split()[1])

                message = message[pos+1:].strip()

                rooms[room_number].chat += f'[{client_username}]: {message}\n'

            elif type == 'join':
                room_number = int(message.split()[1])
                rooms[room_number].followers.add(client_username)



        client_username = ''
        
        buffer = b''
        recv_size = 1024

        while True:

            try:
                # recieve data from user
                data = client.recv(recv_size)
                print(f'received: {data}')

                if data:
                    buffer += data
                    if can_read():
                        read()

                else:
                    raise Error('disconnected')

            except:
                # close the socket
                client.close()
                print('client socket closed\n')




# if run as script
if __name__ == "__main__":
    server = Server('', PORT)
    server.listen()
