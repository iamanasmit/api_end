import socket
import numpy as np
import soundfile as sf
import requests
import time
import os

# ESP32 Network Details
ESP32_IP = "192.168.1.100"  # Replace with the ESP32's IP address
PORT = 80

# Audio Processing Configurations
SR = 16000  # Sample rate
gain = 40  # Gain factor
TRANSCRIBE_URL = "http://127.0.0.1:8000/transcribe/"  # API endpoint
WAKE_WORD = "alexa"  # Wake word

def send_command(command):
    """Send a command to ESP32 over a socket connection."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ESP32_IP, PORT))
        client_socket.send((command + "\n").encode())
        response = client_socket.recv(1024).decode().strip()
        print(f"ESP32 Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def receive_audio(filename="raw_audio.pcm"):
    """Receives audio from ESP32 and saves it as a PCM file."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ESP32_IP, PORT))
        print(f"Connected to ESP32 at {ESP32_IP}:{PORT}")
        
        with open(filename, "wb") as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)

        print(f"Data saved to {filename}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def process_audio(input_file="raw_audio.pcm", output_file="output.wav"):
    """Processes raw PCM audio and saves it as a WAV file."""
    try:
        if not os.path.exists(input_file):
            print(f"Error: {input_file} does not exist.")
            return False

        audio_data = np.fromfile(input_file, dtype=np.int16)
        audio_data = audio_data * gain  # Apply gain
        sf.write(output_file, audio_data, SR)
        print("WAV file saved successfully!")
        return True
    except Exception as e:
        print(f"Error processing audio: {e}")
        return False


def transcribe_audio(filename="output.wav"):
    """Sends the audio file to a transcription service and returns the text."""
    try:
        with open(filename, "rb") as f:
            response = requests.post(TRANSCRIBE_URL, files={"file": f})
        return response.json().get("transcript", "")
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return ""


def process_command(command):
    """Processes voice commands and controls ESP32 devices."""
    command = command.lower().split()
    
    if any(word in command for word in ["light", "lights"]):
        if "on" in command:
            send_command("light on")
        elif "off" in command:
            send_command("light off")
        else:
            print("Could not understand light command.")


def listen_for_wake_word():
    """Continuously listens for the wake word."""
    while True:
        receive_audio("wake_word_audio.pcm")
        if process_audio("wake_word_audio.pcm", "wake_word.wav"):
            transcript = transcribe_audio("wake_word.wav").lower()
            if WAKE_WORD in transcript:
                print("Alexa: Yes?")
                return True
        time.sleep(0.1)  # Short delay before next check


def main():
    """Main loop mimicking Alexa behavior."""
    print("Alexa is listening...")
    while True:
        if listen_for_wake_word():
            print("Alexa: Listening for command...")
            receive_audio("command_audio.pcm")
            if process_audio("command_audio.pcm", "command.wav"):
                command = transcribe_audio("command.wav")
                print(f"Alexa: You said '{command}'")
                process_command(command)
            time.sleep(1)  # Small delay before resuming wake word listening


if __name__ == "__main__":
    main()
