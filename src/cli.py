# Placeholder for CLI logic
import click
import asyncio
from src.audio.audio_handler import record_audio, play_audio, convert_to_mp3
from src.stt.groq_stt import transcribe_audio
from src.llm.groq_llm import generate_response
from src.tts.edge_tts_handler import text_to_speech
from src.utils.config_manager import load_config
from src.utils.logger import log_error, log_chat
from src.conversation.conversation_manager import ConversationManager
import tempfile
import os
import time
from colorama import Fore, init
import datetime


init(autoreset=True) # Initialize colorama

def listen_for_resume(config, conversation, log_file_path):
    """Listens for resume words while paused."""
    global is_paused
    while is_paused:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
            temp_audio_path = temp_audio_file.name
            audio_path = record_audio(temp_audio_path, config["RECORD_TIMEOUT"], config["RECORD_PHRASE_TIME_LIMIT"], )
            if audio_path:
                transcribed_text = transcribe_audio(audio_path, config["GROQ_API_KEY"])
                if transcribed_text:
                   transcribed_text_lower = transcribed_text.lower()
                   if any(word in transcribed_text_lower for word in config["RESUME_WORDS"]):
                      conversation.add_message("user", transcribed_text)
                      llm_response = generate_response(transcribed_text, config["GROQ_LLM_MODEL"], conversation.get_history(), config["SYSTEM_PROMPT"], config["GROQ_API_KEY"])
                      conversation.add_message("assistant", llm_response)
                      print(Fore.CYAN + f"Bot: {llm_response}" + Fore.RESET)
                      with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_tts_file:
                        temp_tts_path = temp_tts_file.name
                        asyncio.run(text_to_speech(llm_response, config["EDGE_TTS_VOICE"], config["EDGE_TTS_RATE"], config["EDGE_TTS_PITCH"], temp_tts_path))
                        play_audio(temp_tts_path)
                      log_chat(transcribed_text, llm_response, log_file_path)
                      os.unlink(temp_tts_path)
                      is_paused = False
                      print(Fore.YELLOW + "Resumed" + Fore.RESET)
                      os.unlink(temp_audio_path)
                      return
                   os.unlink(temp_audio_path)
                else:
                    os.unlink(temp_audio_path)
            time.sleep(0.1)



@click.command()
def main():
    """Runs the voice chatbot."""
    config = load_config()
    if config is None:
        print("Configuration failed. Please check the .env file.")
        return

    conversation = ConversationManager()
    global is_paused
    is_paused = False
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join("logs", "chat_logs", f"chat_{timestamp}.log")


    while True:
        try:
            if is_paused:
                listen_for_resume(config, conversation, log_file_path)
                continue
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio_file:
                temp_audio_path = temp_audio_file.name
                audio_path = record_audio(temp_audio_path, config["RECORD_TIMEOUT"], config["RECORD_PHRASE_TIME_LIMIT"])
                if audio_path:
                    transcribed_text = transcribe_audio(audio_path, config["GROQ_API_KEY"])
                    print(Fore.GREEN + f"You said: {transcribed_text}" + Fore.RESET)
                    if transcribed_text:
                         transcribed_text_lower = transcribed_text.lower()
                         if any(word in transcribed_text_lower for word in config["PAUSE_WORDS"]):
                             conversation.add_message("user", transcribed_text)
                             llm_response = generate_response(transcribed_text, config["GROQ_LLM_MODEL"], conversation.get_history(), config["SYSTEM_PROMPT"], config["GROQ_API_KEY"])
                             conversation.add_message("assistant", llm_response)
                             print(Fore.CYAN + f"Bot: {llm_response}" + Fore.RESET)
                             with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_tts_file:
                                 temp_tts_path = temp_tts_file.name
                                 asyncio.run(text_to_speech(llm_response, config["EDGE_TTS_VOICE"], config["EDGE_TTS_RATE"], config["EDGE_TTS_PITCH"], temp_tts_path))
                                 play_audio(temp_tts_path)
                             log_chat(transcribed_text, llm_response, log_file_path)
                             os.unlink(temp_tts_path)
                             is_paused = True
                             print(Fore.YELLOW + "Paused" + Fore.RESET)
                             continue

                         elif any(word in transcribed_text_lower for word in config["EXIT_WORDS"]):
                             print(Fore.YELLOW + "Exiting" + Fore.RESET)
                             break

                         conversation.add_message("user", transcribed_text)
                         llm_response = generate_response(transcribed_text, config["GROQ_LLM_MODEL"], conversation.get_history(), config["SYSTEM_PROMPT"], config["GROQ_API_KEY"])
                         conversation.add_message("assistant", llm_response)
                         print(Fore.CYAN + f"Bot: {llm_response}" + Fore.RESET)

                         with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_tts_file:
                            temp_tts_path = temp_tts_file.name
                            asyncio.run(text_to_speech(llm_response, config["EDGE_TTS_VOICE"], config["EDGE_TTS_RATE"], config["EDGE_TTS_PITCH"], temp_tts_path))
                            play_audio(temp_tts_path)
                         log_chat(transcribed_text, llm_response, log_file_path)
                         os.unlink(temp_tts_path)
                         os.unlink(temp_audio_path)
                    else:
                        print("No transcription was generated.")
                else:
                    print("No audio was recorded")
        except Exception as e:
            log_error(str(e))
            print(Fore.RED + f"An error occurred: {e}" + Fore.RESET)
            conversation.clear_history()
            time.sleep(1)


if __name__ == '__main__':
    main()