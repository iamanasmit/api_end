import streamlit as st
import whisper

# Load Whisper model
model = whisper.load_model("tiny", device='cuda')

# Streamlit UI
st.title("Audio to Text Transcription using Whisper")

# File uploader
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "opus", "m4a"])

if audio_file is not None:
    # Save the uploaded file temporarily
    with open("temp_audio_file.opus", "wb") as f:
        f.write(audio_file.getbuffer())
    
    # Transcribe audio using Whisper
    result = model.transcribe("temp_audio_file.opus")
    
    # Display transcribed text
    st.header("Transcribed Text")
    st.write(result["text"])
