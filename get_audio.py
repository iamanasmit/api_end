import socket
import time

# ESP32 Access Point IP and Port
ESP32_IP = "192.168.4.1"  # Default IP for ESP32 in AP mode
PORT = 80

# Create a TCP socket

for i in range(200):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Connect to the ESP32
        client_socket.connect((ESP32_IP, PORT))
        print(f"Connected to ESP32 at {ESP32_IP}:{PORT}")

        while True:
            # Receive data from the ESP32
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received data: {data}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
    
    time.sleep(0.001)