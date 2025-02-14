import socket
import numpy as np
import soundfile as sf
import requests
import time
import serial

# ESP32 Network Details
ESP32_IP = "192.168.4.1"  # Change if needed
PORT = 80
ESP32_SERIAL_PORT = "COM8"  # Adjust based on your system

# Audio Processing Configurations
SR = 16000  # Sample rate
gain = 40  # Gain factor
TRANSCRIBE_URL = "http://127.0.0.1:8000/transcribe/"  # API endpoint

# Initialize Serial Connection to ESP32
ser = serial.Serial(ESP32_SERIAL_PORT, 9600, timeout=1)
time.sleep(2)  # Allow ESP32 to initialize

def send_command(command):
    ser.write((command + "\n").encode())
    time.sleep(1)
    response = ser.readline().decode().strip()
    print(f"ESP32 Response: {response}")

def receive_audio():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ESP32_IP, PORT))
        print(f"Connected to ESP32 at {ESP32_IP}:{PORT}")
        
        with open("raw_audio.pcm", "wb") as f:
            for i in range(70):  # Adjust this to capture more/less data
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    # Connect to ESP32
                    client_socket.connect((ESP32_IP, PORT))
                    print(f"Connected to ESP32 at {ESP32_IP}:{PORT}")

                    while True:
                        data = client_socket.recv(1024)  # ✅ Read as binary
                        if not data:
                            break
                        
                        f.write(data)  # ✅ Save raw PCM data

                except Exception as e:
                    print(f"Error: {e}")
                finally:
                    client_socket.close()
                
                time.sleep(0.002)  # Short delay between requests

        print("Data saved to raw_audio.pcm")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def process_audio():
    audio_data = np.fromfile("raw_audio.pcm", dtype=np.int16)
    audio_data = audio_data * gain  # Apply gain
    sf.write("output.wav", audio_data, SR)
    print("WAV file saved successfully!")

def transcribe_audio():
    with open("output.wav", "rb") as f:
        response = requests.post(TRANSCRIBE_URL, files={"file": f})
    return response.json().get("transcript", "")

def process_command(command):
    command = command.lower().split()
    
    if any(word in command for word in ["light.", "lights.", 'light', 'lights']):
        if "on" in command:
            try:
                send_command("light on")
            except:
                pass
        elif "off" in command:
            try:
                send_command("light off")
            except:
                pass

if __name__ == "__main__":
    print("Listening for commands...")
    while True:
        receive_audio()  # Continuously capture audio
        process_audio()  # Convert PCM to WAV
        command = transcribe_audio()  # Speech-to-text
        print(f"Recognized Command: {command}")
        process_command(command)  # Execute action
        time.sleep(1)  # Small delay to prevent overloading
