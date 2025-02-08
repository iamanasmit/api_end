import requests

url = "http://127.0.0.1:8000/transcribe/"
file_path = "test.wav"

with open(file_path, "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)

print(response.json())
