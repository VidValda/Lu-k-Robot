import socket
import time

server_ip = '192.168.97.194'
server_port = 5005

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
count = 0
while True:
    try:
        client_socket.connect((server_ip, server_port))
        print(f"Connected to {server_ip}:{server_port}")

        while True:
            message_to_send = f"Hello, Raspberry Pi! {count}\n"
            client_socket.send(message_to_send.encode('utf-8'))
            count += 1
            time.sleep(0.01)  # Add a delay to control the rate of sending data

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(1)  # Retry the connection after a short delay

    finally:
        client_socket.close()
