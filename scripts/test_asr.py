import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.pipeline.asr import WhisperSpeechRecognizer


def main():
    recognizer = WhisperSpeechRecognizer(model_name="base")

    test_files = {
        "pl": PROJECT_ROOT / "data" / "test_audio" / "input" / "sample_pl.mp3",
        "en": PROJECT_ROOT / "data" / "test_audio" / "input" / "sample_en.mp3",
        "pt": PROJECT_ROOT / "data" / "test_audio" / "input" / "sample_pt.mp3",
    }

    for expected_language, audio_path in test_files.items():
        print("=" * 50)
        print(f"Expected language: {expected_language}")
        print(f"File: {audio_path}")

        try:
            transcript = recognizer.transcribe(str(audio_path), language_code=expected_language)
            print("Transcript:")
            print(transcript)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
