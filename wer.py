import json
from jiwer import wer
from tabulate import tabulate

# Function to calculate WER
def calculate_wer(reference, hypothesis):
    return wer(reference, hypothesis)

# Function to calculate WER for all transcriptions in the JSON file
def calculate_wer_from_json(json_file="wertranscriptions.json"):
    # Load data from the wertranscriptions.json file with UTF-8 encoding
    with open(json_file, "r", encoding="utf-8") as file:
        transcriptions = json.load(file)

    # Initialize variables to calculate total WER
    total_wer = 0
    count = 0
    wer_data = []

    for entry in transcriptions:
        real_transcription = entry["real_transcription"]
        generated_transcription = entry["transcription"]

        # Calculate WER
        error_rate = calculate_wer(real_transcription, generated_transcription)
        total_wer += error_rate
        count += 1

        # Add the current entry to the WER data list
        wer_data.append([entry["filename"], error_rate])

    # Calculate the average WER for all entries
    if count > 0:
        average_wer = total_wer / count
    else:
        average_wer = 0

    # Add summary row to the data
    wer_data.append(["Total", total_wer])
    wer_data.append(["Average", average_wer])

    # Print the results in a table format using tabulate
    headers = ["Filename", "Word Error Rate (WER)"]
    print(tabulate(wer_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    calculate_wer_from_json()