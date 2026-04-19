import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.pipeline.speech_to_speech import SpeechToSpeechPipeline


def main():
    pipeline = SpeechToSpeechPipeline(
        model_path="models/cnn_model.pth",
        whisper_model="base",
    )

    input_dir = PROJECT_ROOT / "data" / "test_audio" / "input"
    output_dir = PROJECT_ROOT / "data" / "test_audio" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    test_files = {
        "pl": input_dir / "sample_pl.mp3",
        "en": input_dir / "sample_en.mp3",
        "pt": input_dir / "sample_pt.mp3",
    }

    target_language = "en"

    for expected_language, audio_path in test_files.items():
        print("=" * 60)
        print(f"Expected language: {expected_language}")
        print(f"Input file: {audio_path}")

        output_path = output_dir / f"{audio_path.stem}_translated_{target_language}.mp3"

        try:
            result = pipeline.run(
                audio_path=str(audio_path),
                target_language=target_language,
                output_path=str(output_path),
            )

            print(f"Detected language: {result['source_language']}")
            print(f"Confidence: {result['confidence']:.4f}")
            print("Probabilities:")
            for lang, prob in result["probabilities"].items():
                print(f"  {lang}: {prob:.4f}")
            print("Transcript:")
            print(result["transcript"])
            print("Translated text:")
            print(result["translated_text"])
            print("Output audio:")
            print(result["output_audio_path"])

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
