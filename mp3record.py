import pyaudio
import wave
import os
from pydub import AudioSegment

# Function to record audio for a given duration (in seconds)
def record_audio(duration=10, output_filename="voice_message.wav"):
    # Set up audio parameters
    FORMAT = pyaudio.paInt16  # Audio format
    CHANNELS = 1              # Mono audio
    RATE = 44100              # Sample rate (44.1kHz)
    CHUNK = 1024              # Number of frames per buffer
    RECORD_SECONDS = duration # Duration to record
    OUTPUT_FILENAME = output_filename

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Start recording
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"Recording for {RECORD_SECONDS} seconds...")

    frames = []

    # Record audio in chunks
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save as WAV
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved as {OUTPUT_FILENAME}.")

# Function to convert WAV file to MP3
def convert_wav_to_mp3(input_wav, output_mp3):
    audio = AudioSegment.from_wav(input_wav)
    audio.export(output_mp3, format="mp3")
    print(f"Converted to {output_mp3}.")

# Main function to record and save the audio
def main():
    # Directory where you want to save the file
    directory = "audio"  # Adjust this as needed

    # Ensure directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Set output WAV and MP3 filenames
    wav_filename = os.path.join(directory, "temp_voice_message.wav")
    mp3_filename = os.path.join(directory, "voice_message.mp3")

    # Record audio for 10 seconds
    record_audio(duration=10, output_filename=wav_filename)

    # Convert the recorded WAV file to MP3
    convert_wav_to_mp3(wav_filename, mp3_filename)

    # Optionally, remove the temporary WAV file
    os.remove(wav_filename)

if __name__ == "__main__":
    main()
