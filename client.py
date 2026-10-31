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
    print(Fore.YELLOW + " [+] Sparrow Secure Internet Chat - Client\n" + Style.RESET_ALL)

def start_client():
    banner()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    host = input(Fore.YELLOW + "Enter Host/IP (or ngrok host): " + Style.RESET_ALL).strip()
    port = int(input(Fore.YELLOW + "Enter Port: " + Style.RESET_ALL).strip())
    
    user = input(Fore.YELLOW + "Enter Username: " + Style.RESET_ALL).strip()
    pwd = input(Fore.YELLOW + "Enter Password: " + Style.RESET_ALL).strip()
    
    print(Fore.BLUE + "[*] Connecting to server..." + Style.RESET_ALL)
    try:
        client.connect((host, port))
        
        # Send Credentials
        client.send(f"{user}:{pwd}".encode())
        auth_status = client.recv(1024).decode()
        
        if auth_status != "AUTH_SUCCESS":
            print(Fore.RED + "[-] Authentication Failed! Incorrect username or password." + Style.RESET_ALL)
            sys.exit(1)
            
        print(Fore.GREEN + "[+] Authenticated & Connected successfully!\n" + Style.RESET_ALL)
    except Exception:
        print(Fore.RED + "[-] Connection failed." + Style.RESET_ALL)
        sys.exit(1)
    
    while True:
        try:
            message = input(Fore.GREEN + "You    : " + Style.RESET_ALL)
            client.send(message.encode())
            
            response = client.recv(1024).decode()
            if not response:
                break
            print(Fore.MAGENTA + f"Friend : {response}" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\n[-] Chat closed." + Style.RESET_ALL)
            break

    client.close()

if __name__ == "__main__":
    start_client()
