import socket

PORT = 5200

sock = socket.socket()
sock.connect(('127.0.0.1', PORT))


class Group():

    def __init__(self, title, tags, goals, is_member):
        self.title = title
        self.tags = tags
        self.goals = goals
        self.is_member = is_member

def login(username):

    load = ('type: username\n'
           f'username: {username}')

    sock.send((f'size: {len(load)}\n' + load).encode())

    return True

def create_page(title, tags, goals):

    load = ('type: create\n'
           f'title: {title}\n'
           f'tags: {tags}\n'
           f'goals: {goals}\n')

    sock.send((f'size: {len(load)}\n' + load).encode())

    return True

def get_groups():

    recv_size = 1024

    load = 'type: rooms\n'

    sock.send((f'size: {len(load)}\n' + load).encode())

    buffer = b''

    while not can_read(buffer):
        data = sock.recv(recv_size)
        
        if data:
            buffer += data

    decoded_buffer = buffer.decode()
    parts = decoded_buffer.split()
    parts = parts[2:]
    print(parts)

    groups = []

    for i in range(int(len(parts)/4)):

        group = Group(parts[4*i+0], parts[4*i+1], parts[4*i+2], parts[4*i+3])
        groups.append(group)

    return groups

def get_chat(room_number):

    recv_size = 1024

    load = ('type: read\n'
           f'room_number: {room_number}')

    sock.send((f'size: {len(load)}\n' + load).encode())

    buffer = b''

    while not can_read(buffer):
        data = sock.recv(recv_size)

        if data:
            buffer += data

    decoded_buffer = buffer.decode()
    pos = decoded_buffer.find('\n')
    chat = decoded_buffer[pos+1:]

    return chat

def send_chat(room_number, message):

    load = ('type: send\n'
           f'room_number: {room_number}\n'
           f'{message.strip()}')

    sock.send((f'size: {len(load)}\n' + load).encode())


def can_read(buffer):

    decoded_buffer = buffer.decode()

    pos = decoded_buffer.find('\n')
    if pos == -1:
        return False

    size = int(decoded_buffer[:pos].split()[1])

    if len(decoded_buffer) - (pos+1) >= size:
        return True
    return False
