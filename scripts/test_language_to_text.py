import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.pipeline.language_to_text import LanguageToTextPipeline


def main():
    pipeline = LanguageToTextPipeline(model_path="models/cnn_model.pth", whisper_model="base")

    test_files = {
        "pl": PROJECT_ROOT / "data" / "test_audio" / "input" / "sample_pl.mp3",
        "en": PROJECT_ROOT / "data" / "test_audio" / "input" / "sample_en.mp3",
        "pt": PROJECT_ROOT / "data" / "test_audio" / "input" / "sample_pt.mp3",
    }

    for expected_language, audio_path in test_files.items():
        print("=" * 60)
        print(f"Expected language: {expected_language}")
        print(f"File: {audio_path}")

        try:
            result = pipeline.run(str(audio_path))
            print(f"Detected language: {result['detected_language']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print("Probabilities:")
            for lang, prob in result["probabilities"].items():
                print(f"  {lang}: {prob:.4f}")
            print("Transcript:")
            print(result["transcript"])

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
