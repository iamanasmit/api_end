import serial
import time

ESP32_PORT = "COM8"  

# Open Serial Connection
ser = serial.Serial(ESP32_PORT, 9600, timeout=1)
time.sleep(2)  # Allow time for ESP32 to initialize

# Function to send command
def send_command(command):
    ser.write((command + "\n").encode())  # Send command
    time.sleep(1)  # Wait for ESP32 response
    response = ser.readline().decode().strip()  # Read response
    print(f"ESP32: {response}")

# Example Commands
for _ in range(5):
    try:
        send_command("light on")
    except:
        print('could not light on')
    try:
        send_command("light off")
    except:
        print('could not light off')

ser.close()