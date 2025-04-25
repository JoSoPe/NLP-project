# NLP Audio Transcription and Intent Detection Project

This project is designed to transcribe MP3 audio files using OpenAI's Whisper model and detect intents using a zero-shot classification approach. It also supports audio recording, transcription, and system call execution based on detected intents.

---

## Features

- **Audio Transcription**: Converts speech in MP3 files to text using the Whisper model.
- **Intent Detection**: Identifies intents from transcriptions using a zero-shot classification model (`facebook/bart-large-mnli`).
- **System Call Execution**: Matches detected intents to predefined system calls and executes them.
- **Audio Recording**: Records audio from a microphone and saves it as an MP3 file.
- **Word Error Rate (WER) Calculation**: Evaluates transcription accuracy by comparing generated transcriptions with real transcriptions.

---

## Folder Structure

```
NLP project/
├── audio/                ← Place your MP3 files here for transcription  
├── processed_mp3/        ← Transcribed MP3 files are moved here  
├── transcribe.py         ← Script for transcribing audio files  
├── mp3record.py          ← Script for recording short audio samples  
├── intent_detection.py   ← Script for detecting intents from transcriptions  
├── integrated_transcribe_intent_detection.py ← Main script for transcription and intent detection  
├── cli_transcribe_execute.py ← CLI-based transcription and intent execution  
├── wer.py                ← Script for calculating Word Error Rate (WER)  
├── requirements.txt      ← List of required Python libraries  
├── environmentsetup.bat  ← Windows setup script for the project  
├── System_calls.json     ← JSON file containing predefined system calls and intents  
├── transcriptions.json   ← JSON file storing transcription results  
├── wertranscriptions.json ← JSON file for WER evaluation  
├── intent_log.json       ← Log file for detected intents  
├── venv/                 ← Virtual environment for the project  
└── readme.txt            ← You're reading it!
```

---

## Setup Instructions

1. **Install Python**:
   - Ensure Python 3.8 or higher is installed and added to your system PATH.

2. **Run the Setup Script**:
   - Execute `environmentsetup.bat` to set up the virtual environment, install dependencies, and verify FFmpeg installation.

   ```cmd
   environmentsetup.bat
   ```

3. **Install FFmpeg**:
   - Download FFmpeg from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/).
   - Extract it and add the `bin` folder to your system PATH.

4. **Activate the Virtual Environment**:
   - On Windows:
     ```cmd
     venv\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

5. **Install Required Libraries**:
   - Install dependencies manually if needed:
     ```bash
     pip install -r requirements.txt
     ```

---

## Usage

### 1. **Transcribe Audio Files**
   - Place your MP3 files in the `audio/` folder.
   - Run the transcription script:
     ```cmd
     python transcribe.py
     ```
   - Transcriptions will be saved in `transcriptions.json`.

### 2. **Record and Transcribe Audio**
   - Use `mp3record.py` to record audio and save it as an MP3 file:
     ```cmd
     python mp3record.py
     ```

### 3. **Transcription and Intent Detection**
   - Use `integrated_transcribe_intent_detection.py` to transcribe audio, detect intents, and match system calls:
     ```cmd
     python integrated_transcribe_intent_detection.py
     ```

### 4. **CLI-Based Transcription and Execution**
   - Use `cli_transcribe_execute.py` for a command-line interface:
     ```cmd
     python cli_transcribe_execute.py --audio <path_to_audio_file>
     ```
   - Or record audio directly:
     ```cmd
     python cli_transcribe_execute.py --record
     ```

### 5. **Calculate Word Error Rate (WER)**
   - Use `wer.py` to calculate WER for transcriptions:
     ```cmd
     python wer.py
     ```

---

## System Calls and Intents

The `System_calls.json` file contains predefined system calls and their corresponding intents. Example:

```json
[
    {
        "system_call": "scan_vulnerabilities(devices='iot')",
        "trigger_phrase": "scan vulnerabilities",
        "intent": "vulnerability_scan"
    },
    {
        "system_call": "check_firewall_status(scope='all_zones')",
        "trigger_phrase": "check firewall status",
        "intent": "check_firewall_status"
    }
]
```

You can modify this file to add or update system calls and intents.

---

## Requirements

- Python 3.8 or higher
- FFmpeg (installed and added to PATH)
- Required Python libraries (see `requirements.txt`)

---

## Troubleshooting

- **FFmpeg Not Found**: Ensure FFmpeg is installed and added to your PATH.
- **Missing Dependencies**: Run `pip install -r requirements.txt` to install all required libraries.
- **Transcription Errors**: Check if the audio file is in the correct format and placed in the `audio/` folder.

---
