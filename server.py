#!/usr/bin/python
# -*- coding: UTF-8 -*-

import socket
import sys

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("Please install colorama: pip3 install colorama")
    sys.exit(1)

def banner():
    print(Fore.CYAN + """
   ██████  ██████   █████  ██████  ██████   ██████  ██     ██
  ██       ██   ██ ██   ██ ██   ██ ██   ██ ██    ██ ██     ██
   █████   ██████  ███████ ██████  ██████  ██    ██ ██  █  ██
        ██ ██      ██   ██ ██   ██ ██   ██ ██    ██ ██ ███ ██
  ██████   ██      ██   ██ ██   ██ ██   ██  ██████   ███ ███ 
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + " [+] Sparrow Secure Internet Chat - Server\n" + Style.RESET_ALL)

def start_server():
    banner()
    
    # Set Username and Password
    SERVER_USER = "sparrow"
    SERVER_PASS = "12345"
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(1)
    print(Fore.GREEN + "[*] Waiting for connection on port 5000..." + Style.RESET_ALL)
    
    conn, addr = server.accept()
    print(Fore.GREEN + f"[+] Connection received from: {addr}" + Style.RESET_ALL)
    
    # Authentication Check
    creds = conn.recv(1024).decode().strip().split(":")
    if len(creds) == 2 and creds[0] == SERVER_USER and creds[1] == SERVER_PASS:
        conn.send("AUTH_SUCCESS".encode())
        print(Fore.GREEN + "[+] Authentication Successful! Chat started.\n" + Style.RESET_ALL)
    else:
        conn.send("AUTH_FAILED".encode())
        print(Fore.RED + "[-] Authentication Failed! Closing connection." + Style.RESET_ALL)
        conn.close()
        server.close()
        return

    while True:
        try:
            message = conn.recv(1024).decode()
            if not message:
                break
            print(Fore.MAGENTA + f"Friend : {message}" + Style.RESET_ALL)
            
            response = input(Fore.GREEN + "You    : " + Style.RESET_ALL)
            conn.send(response.encode())
        except KeyboardInterrupt:
            print(Fore.RED + "\n[-] Chat closed." + Style.RESET_ALL)
            break

    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
