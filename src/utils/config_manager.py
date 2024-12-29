# Placeholder for configuration loading and validation
import os
from dotenv import load_dotenv
import asyncio

def load_config():
    """Loads settings from the .env file, validates them, and returns them as dictionary."""
    load_dotenv()
    config = {}
    try:
        config["SYSTEM_PROMPT"] = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant")
        config["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
        config["GROQ_LLM_MODEL"] = os.getenv("GROQ_LLM_MODEL", "llama3-8b-8192")
        config["EDGE_TTS_VOICE"] = os.getenv("EDGE_TTS_VOICE", "en-US-JennyNeural")
        config["EDGE_TTS_RATE"] = int(os.getenv("EDGE_TTS_RATE", 0))
        config["EDGE_TTS_PITCH"] = int(os.getenv("EDGE_TTS_PITCH", 0))
        config["PAUSE_WORDS"] = os.getenv("PAUSE_WORDS", "hold on,pause,let's take a break").lower().split(",")
        config["RESUME_WORDS"] = os.getenv("RESUME_WORDS", "I'm back,Llamara").lower().split(",")
        config["EXIT_WORDS"] = os.getenv("EXIT_WORDS", "goodbye,that's all for now").lower().split(",")
        config["RECORD_TIMEOUT"] = int(os.getenv("RECORD_TIMEOUT", 10))
        config["RECORD_PHRASE_TIME_LIMIT"] = int(os.getenv("RECORD_PHRASE_TIME_LIMIT", 5))
        config["ENERGY_THRESHOLD"] = int(os.getenv("ENERGY_THRESHOLD", 2000))


        if not config["GROQ_API_KEY"]:
            raise ValueError("GROQ_API_KEY is not set in .env")

        # Validate model against the available models in llm module
        from src.llm.groq_llm import get_available_models
        available_models = get_available_models()
        if config["GROQ_LLM_MODEL"] not in available_models:
            raise ValueError(f"GROQ_LLM_MODEL '{config['GROQ_LLM_MODEL']}' is not a valid model. Choose one of: {', '.join(available_models)}")

        # Validate voices against the available voices in tts module
        from src.tts.edge_tts_handler import get_available_voices
        available_voices = asyncio.run(get_available_voices())
        if config["EDGE_TTS_VOICE"] not in available_voices:
            raise ValueError(f"EDGE_TTS_VOICE '{config['EDGE_TTS_VOICE']}' is not a valid voice. Choose one of: {', '.join(available_voices.values())}") # Changed to check for value in available voices, rather than key
        config["EDGE_TTS_VOICE_FULL"] = available_voices[config["EDGE_TTS_VOICE"]] # load the full voice string

    except ValueError as e:
        print(f"Error in configuration: {e}")
        return None
    return config