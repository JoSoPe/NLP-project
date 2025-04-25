import os
import shutil
import json
import whisper
import platform
from datetime import datetime
from pydub.utils import mediainfo
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
            print(f"Error moving file {mp3_filename}: {e}")
    else:
        print(f"File {source_path} not found.")
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

# ----------- Linear Rule System Call with Cosine Similarity --------------

def match_system_call_directly(text, system_calls):
    # Extract the list of trigger phrases
    trigger_phrases = [entry.get("trigger_phrase", "") for entry in system_calls]
    
    # Create a TF-IDF Vectorizer and calculate cosine similarities
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text] + trigger_phrases)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    # Find the index of the most similar system call
    best_match_index = cosine_similarities.argmax()
    best_match_score = cosine_similarities[best_match_index]
    
    # Return the system call with the highest similarity, or "No Match" if the similarity is too low
    if best_match_score > 0.2:  # Adjust threshold as needed
        return system_calls[best_match_index]["system_call"]
    else:
        return "No Match"

# ----------- Main Integration Logic --------------

def process_transcriptions():
    audio_folder = "audio"
    json_file = "transcriptions.json"
    system_calls_file = "System_calls.json"

    if not os.path.exists(audio_folder):
        print(f"Folder '{audio_folder}' not found.")
        return

    mp3_files = [f for f in os.listdir(audio_folder) if f.lower().endswith(".mp3")]
    if not mp3_files:
        print("No MP3 files to process.")
        return

    model = whisper.load_model("base")
    print("Whisper model loaded.")

    with open(system_calls_file, "r", encoding="utf-8") as f:
        system_calls = json.load(f)

    processed = []

    for mp3 in mp3_files:
        print("\n")
        path = os.path.join(audio_folder, mp3)
        print(f"[+] Transcribing: {mp3}")
        transcription = transcribe_audio(model, path)
        duration = get_audio_duration(path)
        print(f"[+] Transcription: {transcription}")

        # Rule-based system call using Cosine Similarity
        linear_system_call = match_system_call_directly(transcription, system_calls)
        print(f"[+] Linear Rule System Call with Cosine Similarity: {linear_system_call}")

        # Zero-shot intent detection
        detected_intent, score = detect_intent(transcription, [s["intent"] for s in system_calls])
        print(f"[+] Intent detected from transcription: {detected_intent} using facebook/bart-large-mnli model")
        
        # Match system call from detected intent
        matched_call = next((s["system_call"] for s in system_calls if s["intent"] == detected_intent), "No Match")
        print(f"[+] Systemcall from intent detected: {matched_call}")

        processed.append({
            "filename": mp3,
            "transcription": transcription,
            "duration_seconds": duration,
            "transcribed_at": datetime.now().isoformat(),
            "linear_system_call": linear_system_call,
            "intent": detected_intent,
            "intent_score": round(score, 2),
            "matched_system_call": matched_call
        })
            

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(processed, f, indent=4, ensure_ascii=False)

    print(f"\n Processed all MP3s. Results saved to {json_file}")

# ----------- Init & Pipeline --------------

if __name__ == "__main__":
    import torch
    print("Using GPU:" if torch.cuda.is_available() else "Running on CPU")
    set_ffmpeg_path()
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    process_transcriptions()
    print(f" Moved files to processed_mp3 folder\n")