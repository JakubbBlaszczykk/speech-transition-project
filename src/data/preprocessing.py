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

        # MFCC
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)

        # DELTA (time changes)
        delta = librosa.feature.delta(mfcc)

        # STACK (80 x time)
        features = np.vstack([mfcc, delta])

        # NORMALIZATION
        std = np.std(features)
        if std == 0:
            std = 1e-6

        features = (features - np.mean(features)) / std

        # save
        np.save(output_path, features)

    except Exception as e:
        print("Error:", file_path, e)


def process_folder(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    files = [f for f in os.listdir(input_dir) if f.endswith(".mp3")]

    print(f"Processing {input_dir}, found {len(files)} files")

    for file in tqdm(files):
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file.replace(".mp3", ".npy"))

        process_file(input_path, output_path)
        


if __name__ == "__main__":
    process_folder("data/raw/pl", "data/processed/pl")
    process_folder("data/raw/pt", "data/processed/pt")
    process_folder("data/raw/en", "data/processed/en")