import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

with open('config.json') as json_file:
    config = json.load(json_file)

template_reset = ''
with open('template.txt') as file:
    template_reset = file.read()

with open('chat.txt', 'w') as file:
    file.write(template_reset)

def get_new_connections():
    #funkcja tworząca nowe połączenia i pobierająca dane od klientów
    while True:
        client, client_address = SERVER.accept()
        print('%s:%s...został podłączony' % client_address)

        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    global user_count
    user_count += 1
    name = 'Użytkownik ' + str(user_count)
    welcome = 'Witaj %s!' % name
    client.send(bytes(welcome, 'utf8'))
    msg = '%s dołączył do czatu ;)' % name
    broadcast(bytes(msg, 'utf8'))
    clients[client] = name

    with open('chat.txt', 'a', encoding='utf8') as file:
        file.write(msg+'\n')

    while True:
       msg = client.recv(BUFSIZE)
       if msg != bytes('{quit}', 'utf8'):
           broadcast(msg, name+': ')

           with open('chat.txt', 'a', encoding='utf8') as file:
               file.write(name + ':' + msg.decode("utf8") + '\n' )
       else:
            client.close()
            del clients[client]
            broadcast(bytes('%s opuścił czat.' % name, 'utf8'))
            with open('chat.txt', 'a', encoding='utf8') as file:
                file.write(name + ' opuścił czat.' + '\n')
            break

def broadcast(msg, prefix=''):
    for client in clients:
        client.send(bytes(prefix, 'utf8')+msg)

clients = {}
addresses = {}
user_count = 0

HOST = config['ip']
PORT = config['port']
BUFSIZE = 1024
ADDR = (HOST, PORT)

#Utworzenie soketu TCP/IP
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

#Część główna programu
if __name__ == '__main__':
    SERVER.listen(5)
    print('Oczekiwanie na połączenie...')
    ACCEPT_THREAD = Thread(target=get_new_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()