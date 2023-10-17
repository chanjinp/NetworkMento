import socket
# thread를 사용하기 때문에 선언
from _thread import *

import threaded

client_sockets_list = []  # 클라이언트가 thread를 사용해서 돌아가기에 다수 접속 가능 => 배열로 관리

# Server IP and Port setting
Host = socket.gethostbyname(socket.gethostname())
Port = 999


def thread(client_socket, addr):
    # >> Connected by: Client[IP] : Client[Port]
    print('>> Connected by: ', addr[0], ':', addr[1])

    # Process until Client Disconnect
    while True:
        try:
            # send Client if data recieved(echo)
            #1024 바이트 크기만큼 client socket에서 데이터 받음
            data = client_socket.recv(1024)
            
            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break
                
            #client의 IP와 Port에서 해당 데이터 직렬화를 풀어서 print시켜줌
            print('>> Received from ' + addr[0], ':', addr[1], data.decode())

            #chat to client connecting client
            #chat to client connecting client except person sending message
            for client in client_sockets_list:
                if (client != client_socket):
                    client.send(data)
        except ConnectionError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break
    if(client_socket in client_sockets_list) :
        client_sockets_list.remove(client_socket)
        print('remove client list : ', len(client_sockets_list))

    client_socket.close()

# Create Socket and Bind

print('>> Server Start with ip :', Host)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((Host, Port))
server_socket.listen()

# Client Socket Accept

try:
    while True:
        print('>> Wait')

        client_socket, addr = server_socket.accept()
        client_sockets_list.append(client_socket)
        start_new_thread(thread, (client_socket, addr))
        print("참가자 수 :", len(client_sockets_list))
except Exception as e:
    print('Error : ', e)

finally:
    server_socket.close()