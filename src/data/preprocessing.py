import os
import librosa
import numpy as np
import random
from tqdm import tqdm


def process_file(file_path, output_path):
    try:
        audio, sr = librosa.load(file_path, sr=16000)

        # skip too short audio files
        if len(audio) < 3 * sr:
            return

        # random fragment of 3 seconds
        start = random.randint(0, len(audio) - 3 * sr)
        audio = audio[start:start + 3 * sr]

        # mel spectrogram
        spec = librosa.feature.melspectrogram(y=audio, sr=sr)
        spec_db = librosa.power_to_db(spec, ref=np.max)

        # normalzation 
        spec_db = (spec_db - np.mean(spec_db)) / np.std(spec_db)

        # save
        np.save(output_path, spec_db)

    except Exception as e:
        print("Error:", file_path, e)


def process_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith(".mp3")]

    for file in tqdm(files):
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file.replace(".mp3", ".npy"))

        process_file(input_path, output_path)


if __name__ == "__main__":
    process_folder("data/raw/pl", "data/processed/pl")
    process_folder("data/raw/pt", "data/processed/pt")
    process_folder("data/raw/en", "data/processed/en")