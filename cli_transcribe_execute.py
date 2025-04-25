import os
import shutil
import json
import whisper
import platform
from datetime import datetime
from pydub.utils import mediainfo
from transformers import pipeline
import argparse
import pyaudio
import wave
import time

# ----------- Setup Section --------------
def set_ffmpeg_path():
    if platform.system() == "Windows":
        ffmpeg_path = r"E:\Download\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\bin"
        os.environ["PATH"] += os.pathsep + ffmpeg_path

def get_audio_duration(file_path):
    try:
        info = mediainfo(file_path)
        return round(float(info.get("duration", 0)), 2)
    except:
        return None

def move_mp3_file(mp3_filename):
    processed_folder = "processed_mp3"
    os.makedirs(processed_folder, exist_ok=True)

    source_path = os.path.join("audio", mp3_filename)
    destination_path = os.path.join(processed_folder, mp3_filename)

    if os.path.exists(source_path):
        try:
            shutil.move(source_path, destination_path)
            return True
        except Exception as e:
            print(f" Error moving file {mp3_filename}: {e}")
    else:
        print(f" File {source_path} not found.")
    return False

# ----------- Transcription & Detection --------------
def transcribe_audio(model, file_path):
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

def detect_intent(text, candidate_labels):
    result = classifier(text, candidate_labels)
    return result['labels'][0], result['scores'][0]

def match_system_call_directly(text, system_calls):
    text = text.lower()
    for entry in system_calls:
        if entry.get("trigger_phrase") and entry["trigger_phrase"].lower() in text:
            return entry["system_call"]
    return "No Match"

# ----------- Main Integration Logic --------------
def process_audio(file_path):
    audio_folder = "audio"
    json_file = "transcriptions.json"
    system_calls_file = "System_calls.json"

    if not os.path.exists(audio_folder):
        print(f" Folder '{audio_folder}' not found.")
        return

    model = whisper.load_model("base")
    print("Whisper model loaded.")

    with open(system_calls_file, "r", encoding="utf-8") as f:
        system_calls = json.load(f)

    transcription = transcribe_audio(model, file_path)
    print(f"Transcription: {transcription}")

    # Rule-based system call
    linear_system_call = match_system_call_directly(transcription, system_calls)
    print(f"Linear Rule System Call with Cosine Similarity: {linear_system_call}")

    # Zero-shot intent detection
    detected_intent, score = detect_intent(transcription, [s["intent"] for s in system_calls])
    print(f"Intent detected from transcription: {detected_intent} using facebook/bart-large-mnli model")
    matched_call = next((s["system_call"] for s in system_calls if s["intent"] == detected_intent), "No Match")
    print(f"Systemcall from intent detected: {matched_call}")

    # Prompt user for confirmation
    print("\nPlease confirm the execution of the following command:")
    print(f"Detected Intent: {detected_intent}")
    print(f"Matched Command: {matched_call}")
    confirmation = input("Do you want to execute this command? (y/n): ").strip().lower()

    if confirmation == "y":
        # Execute system call
        print(f"Executing system call: {matched_call}")
        # You can call the actual function here using eval() or a safe mapping
        # Example: eval(matched_call) or function_mapping[matched_call]()
        move_mp3_file(file_path)  # Move file to processed folder
        print("File moved to processed_mp3 folder.")
    else:
        print("Execution canceled.")

# ----------- Audio Recording Section --------------
def record_audio(output_file="audio.wav", duration=5):
    print("Recording... Please speak now.")
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                    input=True, frames_per_buffer=1024)
    frames = []

    for _ in range(0, int(16000 / 1024 * duration)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

    return output_file

# ----------- CLI Interface --------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Speech to Command Execution CLI")
    parser.add_argument('--audio', type=str, help="Path to audio file (WAV/MP3)")
    parser.add_argument('--record', action='store_true', help="Record audio from microphone")

    args = parser.parse_args()

    set_ffmpeg_path()
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    while True:
        if args.audio:
            process_audio(args.audio)
        elif args.record:
            audio_file = record_audio("audio.wav", duration=5)  # Default 5 seconds
            process_audio(audio_file)
        else:
            print("No input provided. Please provide either --audio or --record.")

        # Wait for next command or exit
        continue_running = input("\nDo you want to process another command? (y/n): ").strip().lower()
        if continue_running != 'y':
            print("Exiting program.")
            break