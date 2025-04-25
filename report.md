# Short Report

## Recap of Objectives and Approach

The primary objective of this project was to develop a system capable of transcribing audio files into text using OpenAI's Whisper model and detecting intents from the transcriptions using a zero-shot classification approach. The system was designed to support additional functionalities such as audio recording, transcription accuracy evaluation (via Word Error Rate), and executing predefined system calls based on detected intents. The overarching goal was to create an integrated pipeline that could process audio inputs and perform automated actions based on natural language commands.

## Implementation Details (and Changes from Proposal)

1. **Audio Transcription**:
   - The transcription process was implemented using OpenAI's Whisper model. The model was loaded and used to transcribe MP3 audio files placed in the `audio/` directory. The transcriptions were saved in a JSON file (`transcriptions.json`) for further processing. No model training or fine-tuning was required; only local inference with the "base" model was used.

2. **Intent Detection**:
   - Intent detection was achieved using a zero-shot classification model (`facebook/bart-large-mnli`) from the Hugging Face Transformers library. The transcriptions were analyzed to identify the most relevant intent from a predefined list of candidate intents. When the transcription closely matched a predefined template (rule-based), it was mapped directly.

3. **System Call Execution**:
   - A mapping of intents to system calls was defined in a JSON file (`System_calls.json`). Detected intents were matched to their corresponding system calls, which could then be executed programmatically, with user confirmation provided via a CLI interface.

4. **Audio Recording**:
   - A script (`mp3record.py`) was implemented to record audio from a microphone, save it as a WAV file, and convert it to MP3 format for transcription. Recording is also supported directly from the CLI interface for user convenience.

5. **Word Error Rate (WER) Calculation**:
   - The transcription accuracy was evaluated using the `jiwer` library. Real (reference) transcriptions were compared with generated transcriptions, and the WER was calculated and displayed in a tabular format. This metric provided a quantitative way to evaluate ASR performance.

6. **Cosine Similarity Matching (Added Feature):**
   - To improve matching, especially in ambiguous cases, a TF-IDF cosine similarity approach was integrated. This method helps associate user transcriptions with the closest command template when zero-shot classification confidence is low or the language is fuzzy.

7. **Folder Structure and Automation**:
   - The project was organized into folders for audio files, processed files, and virtual environment setup. A batch script (`environmentsetup.bat`) was created to automate the setup process, including installing dependencies and verifying FFmpeg installation.

## Demonstration of Results (Metrics and Examples)

- **Transcription Accuracy:**
  - Word Error Rate (WER) was evaluated using sample files. For example, a clean English phrase such as "Today is a beautiful day to learn something new." resulted in a WER of 0%. Noisy audio or phrases with uncommon words produced higher WER.
  - Quantitative results for 9 test audios are logged in `wertranscriptions.json`.

- **Intent Detection and System Call Mapping:**
  - Example: For the audio "Check if the firewall is active across all the network zones.", the transcription matched the intent `check_firewall_status`, leading to the system call `check_firewall_status(scope='all_zones')`.
  - All processed results, including intent, score, and system call, are saved in `transcriptions.json`.
  - Confidence scores are logged for further analysis.

- **User Interaction:**
  - The CLI prompts for confirmation before executing detected system calls. Users can interactively record audio and trigger the processing pipeline in real time.

## Reflections on Challenges and Improvements

### Challenges:
- **FFmpeg Integration:** Ensuring FFmpeg was correctly installed and accessible in the system PATH was a recurring issue, particularly for users less familiar with command-line environments.
- **Transcription Accuracy:** Although Whisper performs well, lower quality audio (e.g., background noise or unclear speech) decreased accuracy and affected intent detection. Additionally, even though the zero-shot classification model (`facebook/bart-large-mnli`) was used, some transcriptions were not accurate, which impacted the intent detection process.
- **Intent Detection Limitations:** The zero-shot model sometimes produced low-confidence or incorrect intents, especially with ambiguous or novel speech patterns.
- **System Call Mapping:** Careful design of intent-to-system-call mapping was necessary to avoid mismatches or unintended commands.

### Improvements:
- **Enhanced Error Handling:** The system was improved to provide clearer feedback for missing dependencies, invalid audio, or processing errors.
- **Cosine Similarity Fallback:** The addition of TF-IDF cosine similarity provided a fallback mechanism for matching commands, increasing robustness in intent-to-command association.
- **WER Evaluation:** Including WER evaluation enabled a measurable assessment of system performance, helping identify strengths and weaknesses.
- **User-Centric CLI:** Developing an interactive CLI improved usability, allowing users to record, process, and confirm actions in a single workflow.

Overall, the project successfully demonstrated an end-to-end pipeline for speech-based intent detection and automated action execution. The design is modular and extensible, providing a foundation for further development, such as improved parameter extraction, support for more commands, and deeper integration with external systems.