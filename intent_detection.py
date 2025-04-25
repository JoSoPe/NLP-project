import json
from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def detect_intent(text, candidate_labels):
    # Perform zero-shot classification
    result = classifier(text, candidate_labels)
    
    # Return the most likely intent and its score
    return result['labels'][0], result['scores'][0]  # Return the most likely intent and its score

def read_transcriptions():
    # Read the transcriptions from the JSON file
    try:
        with open('transcriptions.json', 'r', encoding='utf-8') as file:
            transcriptions = json.load(file)
        return transcriptions
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error reading transcriptions.json or file is empty.")
        return []

def write_transcription_log(log_entry):
    # Write the log entry (with intent) to a transcription log
    try:
        with open('intent_log.json', 'a', encoding='utf-8') as log_file:
            json.dump(log_entry, log_file, ensure_ascii=False, indent=4)
            log_file.write("\n")
    except Exception as e:
        print(f"Error writing to intent_log.json: {e}")

def update_transcriptions(transcriptions):
    # Update the transcriptions by removing the processed transcription
    try:
        with open('transcriptions.json', 'w', encoding='utf-8') as file:
            json.dump(transcriptions, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing updated transcriptions: {e}")

def process_transcriptions():
    # Load transcriptions
    transcriptions = read_transcriptions()

    if not transcriptions:
        print("No transcriptions to process.")
        return

    # List of possible candidate labels (intents)
    candidate_labels = ["book_flight", "check_weather", "order_food", "play_music"]

    # Process each transcription
    for transcription in transcriptions:
        text = transcription.get('transcription', '')
        if not text:
            continue  # Skip empty transcriptions

        # Detect intent
        detected_intent, score = detect_intent(text, candidate_labels)

        # Prepare the log entry
        log_entry = {
            "filename": transcription['filename'],
            "transcription": transcription['transcription'],
            "real_transcription": transcription['real_transcription'],
            "detected_intent": detected_intent,
            "intent_score": score,
            "processed_at": transcription.get('transcribed_at')
        }

        # Write to the log
        write_transcription_log(log_entry)

        # Remove the processed transcription from the list
        transcriptions.remove(transcription)

    # Update the `transcriptions.json` file after processing
    update_transcriptions(transcriptions)

if __name__ == "__main__":
    process_transcriptions()