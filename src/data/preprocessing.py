import os
import librosa
import numpy as np
import random
from tqdm import tqdm

SAMPLE_RATE = 16000
SEGMENT_SECONDS = 3
SEGMENT_SAMPLES = SAMPLE_RATE * SEGMENT_SECONDS
N_MFCC = 40


def compute_features(audio, sr=SAMPLE_RATE):
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=N_MFCC)
    delta = librosa.feature.delta(mfcc)
    features = np.vstack([mfcc, delta])

    std = np.std(features)
    if std == 0:
        std = 1e-6

    return (features - np.mean(features)) / std


def extract_features(file_path, random_crop=False):
    audio, sr = librosa.load(file_path, sr=SAMPLE_RATE)

    if len(audio) < SEGMENT_SAMPLES:
        raise ValueError(f"Audio file is too short. Required at least {SEGMENT_SECONDS} seconds.")

    if random_crop:
        start = random.randint(0, len(audio) - SEGMENT_SAMPLES)
    else:
        start = max((len(audio) - SEGMENT_SAMPLES) // 2, 0)

    audio = audio[start:start + SEGMENT_SAMPLES]
    return compute_features(audio, sr=sr)

def process_file(file_path, output_path):
    try:
        features = extract_features(file_path, random_crop=True)
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