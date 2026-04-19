import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.model.inference import LanguageClassifier


def main():
    classifier = LanguageClassifier("models/cnn_model.pth")

    test_files = {
        "pl": "data/test_audio/input/sample_pl.mp3",
        "en": "data/test_audio/input/sample_en.mp3",
        "pt": "data/test_audio/input/sample_pt.mp3",
    }

    for expected_language, audio_path in test_files.items():
        print("=" * 50)
        print(f"Expected: {expected_language}")
        print(f"File: {audio_path}")

        try:
            result = classifier.predict(audio_path)
            predicted_language = result["language"]
            confidence = result["confidence"]

            print(f"Predicted: {predicted_language}")
            print(f"Confidence: {confidence:.4f}")
            print("Probabilities:")
            for lang, prob in result["probabilities"].items():
                print(f"  {lang}: {prob:.4f}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
