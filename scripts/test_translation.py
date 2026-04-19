import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.pipeline.translator import TranslatorBackend


def main():
    translator = TranslatorBackend()

    test_sentences = [
        ("pl", "en", "Raz przyniósł fotografię porn."),
        ("en", "pl", "The clouds here are white and puffy like cotton balls."),
        ("pt", "en", "Quente diz que perguntou ao menino assustado."),
    ]

    for source_language, target_language, text in test_sentences:
        print("=" * 60)
        print(f"Source language: {source_language}")
        print(f"Target language: {target_language}")
        print(f"Input text: {text}")

        try:
            translated = translator.translate(
                text=text,
                source_language=source_language,
                target_language=target_language,
            )
            print("Translated text:")
            print(translated)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
