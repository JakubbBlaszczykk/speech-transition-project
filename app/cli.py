import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.pipeline.speech_to_speech import SpeechToSpeechPipeline


def build_parser():
    parser = argparse.ArgumentParser(
        description="Run the speech-to-speech pipeline for an audio file."
    )
    parser.add_argument(
        "audio_path",
        help="Path to the input audio file, for example data/test_audio/input/sample_pt.mp3.",
    )
    parser.add_argument(
        "--target-language",
        default="en",
        choices=["pl", "en", "pt"],
        help="Target language for translation and speech synthesis.",
    )
    parser.add_argument(
        "--output-path",
        default=None,
        help="Optional path for the generated output .mp3 file.",
    )
    parser.add_argument(
        "--model-path",
        default="models/cnn_model.pth",
        help="Path to the trained language classification model.",
    )
    parser.add_argument(
        "--whisper-model",
        default="base",
        help="Whisper model size to use, for example tiny, base, small.",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    pipeline = SpeechToSpeechPipeline(
        model_path=args.model_path,
        whisper_model=args.whisper_model,
    )
    result = pipeline.run(
        audio_path=args.audio_path,
        target_language=args.target_language,
        output_path=args.output_path,
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
