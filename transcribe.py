import whisper
import os
import platform
import json
from datetime import datetime
from pydub.utils import mediainfo

# Set FFmpeg path explicitly if needed
def set_ffmpeg_path():
    if platform.system() == "Windows":
        ffmpeg_path = r"E:\Download\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\ffmpeg-2025-04-21-git-9e1162bdf1-full_build\bin"
        os.environ["PATH"] += os.pathsep + ffmpeg_path
    else:
        ffmpeg_path = "/usr/local/bin"
        os.environ["PATH"] += os.pathsep + ffmpeg_path

# Check if FFmpeg is installed and in PATH
def check_ffmpeg():
    return os.system("ffmpeg -version >nul 2>&1") == 0

# Load the Whisper model
def load_model():
    return whisper.load_model("base")

# Transcribe a single audio file and return transcription data
def transcribe_audio(model, file_path):
    try:
        result = model.transcribe(file_path)
        duration_sec = get_audio_duration(file_path)
        return {
            "filename": os.path.basename(file_path),
            "transcription": result["text"],
            "duration_seconds": duration_sec,
            "transcribed_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "filename": os.path.basename(file_path),
            "error": str(e),
            "transcribed_at": datetime.now().isoformat()
        }

# Get audio duration using pydub/ffmpeg
def get_audio_duration(file_path):
    try:
        info = mediainfo(file_path)
        duration_sec = float(info.get("duration", 0))
        return round(duration_sec, 2)
    except:
        return None

if __name__ == "__main__":
    set_ffmpeg_path()

    if not check_ffmpeg():
        print("FFmpeg is not installed or not in your PATH. Please install it to proceed.")
        exit(1)

    audio_folder = "audio"
    output_file = "transcriptions.json"

    if not os.path.exists(audio_folder):
        print(f"The folder '{audio_folder}' does not exist.")
        exit(1)

    mp3_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(".mp3")]
    if not mp3_files:
        print("No .mp3 files found in the 'audio' folder.")
        exit(0)

    model = load_model()

    all_transcriptions = []

    for mp3_file in mp3_files:
        file_path = os.path.join(audio_folder, mp3_file)
        print(f"🔊 Transcribing: {mp3_file}")
        transcription_data = transcribe_audio(model, file_path)
        all_transcriptions.append(transcription_data)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_transcriptions, f, ensure_ascii=False, indent=4)

    print(f"\n✅ All transcriptions saved to: {output_file}")