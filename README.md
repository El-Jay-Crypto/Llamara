# Llamara - A Voice-Enabled Conversational Chatbot
![image](https://github.com/El-Jay-Crypto/Llamara/blob/main/Llamara.png)

Llamara is a voice-based chatbot application that leverages the power of Groq's low-latency Language Processing Units (LPUs) for speech-to-text (STT) and large language model (LLM) processing, and Microsoft Edge's Text-to-Speech (TTS) for audio output. It provides a command-line interface (CLI) for easy interaction and is designed to be highly configurable via a `.env` file.

## Features

*   **Voice Input:** Record audio directly from your microphone, using a dynamic silence detection algorithm to automatically determine the end of speech.
*   **Groq STT:** Transcribe the recorded audio into text using Groq's fast Whisper-large-v3 implementation.
*   **Groq LLM:** Use Groq's Llama 3.2 LLM models (8B and 70B parameters) to generate conversational responses based on user input and conversation history.
*   **Edge TTS:** Convert the LLM's text responses into natural-sounding speech using Microsoft Edge's Text-to-Speech service.
*   **Continuous Conversation:** The chatbot supports continuous conversation, meaning that it is constantly listening to the user.
*   **Configurable Pause/Resume/Exit:** Use specific words to pause and resume the conversation with a response from the LLM.
*   **Configurable Parameters:** Almost all aspects of the chatbot are configurable via environment variables in a `.env` file.
*   **Conversation Logging:** Chat input and output are logged in separate, timestamped files within a `chat_logs` folder.
*   **Error Logging:** Errors are logged to a separate `error.log` file.
*   **Log Rotation:** Old chat log files are automatically deleted when the number of log files exceeds 10.

## Getting Started

### Prerequisites

*   **Python 3.10 or higher**
*	**Portaudio19-dev & FFmpeg** (`sudo apt install portaudio19-dev ffmpeg`)
*   **A Groq API key** [Get yours here](https://console.groq.com/login)
*   **A microphone connected to your computer**
*   **An internet connection**

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/El-Jay-Crypto/Llamara.git
    cd Llamara
    ```
2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv .venv
    source .venv/bin/activate   # On Linux/macOS
    .venv\Scripts\activate   # On Windows
    ```
3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up the `.env` file:**
    *   Copy `example.env` to `.env`:
        ```bash
        cp example.env .env
        ```
    *   Add your Groq API key, and other configuration parameters to the `.env` file.

### Running the Application

To start the chatbot, simply run the main python program:

```bash
python run.py
```
You can now speak into your microphone to interact with the chatbot.

## Controlling the Chatbot
- **Pause:** Use the following words: "Let's take a break".
- **Resume:** Use the following words: "I'm back".
- **Exit:** Use the following words: "Goodbye".

These words are also configurable via the .env file.

## Configuration Options
The following settings can be configured via environment variables in the .env file:
- **SYSTEM_PROMPT:** Sets the initial prompt for the LLM.
- **GROQ_API_KEY:** Your Groq API key, required for accessing the Groq API.
- **GROQ_LLM_MODEL:** Select a Groq Llama model.
- **EDGE_TTS_VOICE:** Select a US language voice from Edge TTS.
- **EDGE_TTS_RATE:** Sets the speed of the Edge TTS output as a percentage.
- **EDGE_TTS_PITCH:** Sets the pitch of the Edge TTS output in Hz.
- **PAUSE_WORDS:** A comma-separated list of words to pause the chatbot.
- **RESUME_WORDS:** A comma-separated list of words to resume the chatbot.
- **EXIT_WORDS:** A comma-separated list of words to exit the chatbot.
- **RECORD_TIMEOUT:** The maximum time the microphone listens before a phrase starts.
- **RECORD_PHRASE_TIME_LIMIT:** The maximum time for a phrase to be recorded in seconds.
- **ENERGY_THRESHOLD:** The minimum energy of a sound to be considered as speech.

## Project Structure
```
Llamara/
├── src/
│   ├── audio/
│   │   ├── audio_handler.py            # Handles audio recording, detection, and playback
│   ├── stt/
│   │   ├── groq_stt.py                 # Handles Groq STT API calls
│   ├── llm/
│   │   ├── groq_llm.py                 # Handles Groq LLM API calls
│   ├── tts/
│   │   ├── edge_tts_handler.py         # Manages Edge TTS operations
│   ├── utils/
│   │   ├── config_manager.py           # Loads and validates configuration from .env
│   │   ├── logger.py                   # Handles logging to files
│   ├── conversation/
│   │   ├── conversation_manager.py     # Manages conversation history
│   ├── cli.py                          # Command-line interface logic
├── .env                                # Configuration file
├── example.env                         # Example configuration file
├── run.py                              # Main application entry point
├── requirements.txt                    # Python package dependencies
├── .gitignore                          # Git ignore file
└── README.md                           # Project documentation
```
## Dependencies
- `click`: For building command-line interfaces.
- `colorama`: For colored output in the command line.
- `edge-tts`: For Microsoft Edge Text-to-Speech.
- `groq`: For using the Groq API.
- `langchain-community`: For the new langchain community library.
- `pyaudio`: For audio input/output.
- `pydub`: For working with audio file formats.
- `pygame`: For audio playback.
- `python-dotenv`: For loading environment variables from the `.env` file.
- `speechrecognition`: For capturing audio input.

## Contributing
If you would like to contribute, please follow these guidelines:
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them.
- Push your changes to your fork.
- Submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Authors
@El-Jay-Crypto

## Acknowledgments
Special thanks to the developers of Groq, Microsoft Edge TTS, LangChain, and all the Python libraries that made this project possible.

Inspiration was taken from the [Verbi](https://github.com/PromtEngineer/Verbi) project by @PromtEngineer.
