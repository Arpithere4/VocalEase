# VocalEase

VocalEase is a Python-based application that provides text-to-speech (TTS) and speech-to-text (STT) functionalities with additional features like saving audio and text files, and multi-language translation (including support for Indian languages). This application is designed with a futuristic GUI using wxPython.

## Features

- **Text-to-Speech (TTS)**: Convert typed text into spoken words using the `pyttsx3` engine.
- **Speech-to-Text (STT)**: Convert spoken words into text using the `speech_recognition` module.
- **Save Files**: Save converted text and audio files.
- **Multi-language Translation**: Translate text into multiple languages, including Indian languages.
- **Customizable Interface**: A sleek and futuristic GUI built with wxPython.

## Future Features

- Dark Mode and High Contrast Mode.
- Emotion in speech.
- Drag and drop functionality.
- Font size adjustments.
- Animations and transitions for an improved user experience.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/Arpithere4/VocalEase/
    ```

2. Navigate into the project directory:
    ```bash
    cd VocalEase
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python vocalease.py
    ```

## Requirements

- Python 3.7 or higher
- wxPython
- pyttsx3
- speech_recognition
- pyaudio
- googletrans
- gTTS 
## Usage

1. Start the application.
2. Choose between text-to-speech or speech-to-text mode.
3. For speech-to-text, ensure your microphone is connected.
4. Enter text or speak into the microphone for conversion.
5. Save your results as a text or audio file.
6. Use the translation tab to translate your text into multiple languages.

## Contributors

- Arpit Mishra
## License

VocalEase is licensed under the **GNU General Public License v3.0**. This means you are free to copy, modify, and distribute this software, provided that any distribution, including modifications, is also licensed under the GPL.

You can read the full license here: [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

```plaintext
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
