import os
from pathlib import Path

CONDA_FFMPEG_DIR = Path(r"C:\Users\jakub\anaconda3\envs\speech-env\Library\bin")
if CONDA_FFMPEG_DIR.exists():
    os.environ["PATH"] = str(CONDA_FFMPEG_DIR) + os.pathsep + os.environ.get("PATH", "")

try:
    import whisper
except ImportError as e:
    raise ImportError(
        "Package 'openai-whisper' is not installed. "
        "Install it in your active conda environment before running ASR."
    ) from e


class WhisperSpeechRecognizer:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path, language_code=None):
        result = self.model.transcribe(
            audio_path,
            language=language_code,
            task="transcribe",
        )
        return result["text"].strip()
