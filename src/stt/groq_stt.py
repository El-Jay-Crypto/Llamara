# Placeholder for Groq STT API calls
import os
from groq import Groq


def transcribe_audio(audio_file_path, groq_api_key):
    """Sends the audio file to Groq's STT API and returns the transcription."""
    try:
        client = Groq(api_key=groq_api_key)
        with open(audio_file_path, "rb") as file:
            translation = client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3-turbo",  # Or other whisper model like "whisper-large-v3"
            )
            return translation.text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None