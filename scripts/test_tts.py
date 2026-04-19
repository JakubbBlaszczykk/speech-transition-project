import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.pipeline.tts import TTSBackend


def main():
    tts = TTSBackend()

    output_dir = PROJECT_ROOT / "data" / "test_audio" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    test_cases = [
        ("en", "The clouds here are white and puffy like cotton balls.", output_dir / "sample_en_tts.mp3"),
        ("pl", "Chmury tutaj są białe i puszyste jak waciki.", output_dir / "sample_pl_tts.mp3"),
        ("pt", "Quente diz que perguntou ao menino assustado.", output_dir / "sample_pt_tts.mp3"),
    ]

    for language, text, output_path in test_cases:
        print("=" * 60)
        print(f"Language: {language}")
        print(f"Text: {text}")
        print(f"Output path: {output_path}")

        try:
            saved_path = tts.synthesize(
                text=text,
                language=language,
                output_path=str(output_path),
            )
            print("Saved audio:")
            print(saved_path)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
