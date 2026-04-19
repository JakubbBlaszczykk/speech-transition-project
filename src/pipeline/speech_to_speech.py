from pathlib import Path

from src.model.inference import LanguageClassifier
from src.pipeline.asr import WhisperSpeechRecognizer
from src.pipeline.translator import TranslatorBackend
from src.pipeline.tts import TTSBackend


class SpeechToSpeechPipeline:
    def __init__(self, model_path, whisper_model="base"):
        self.classifier = LanguageClassifier(model_path=model_path)
        self.recognizer = WhisperSpeechRecognizer(model_name=whisper_model)
        self.translator = TranslatorBackend()
        self.tts = TTSBackend()

    def run(self, audio_path, target_language="en", output_path=None):
        prediction = self.classifier.predict(audio_path)
        source_language = prediction["language"]

        transcript = self.recognizer.transcribe(
            audio_path,
            language_code=source_language,
        )

        translated_text = self.translator.translate(
            text=transcript,
            source_language=source_language,
            target_language=target_language,
        )

        if output_path is None:
            output_path = f"{Path(audio_path).stem}_{target_language}.mp3"

        saved_audio_path = self.tts.synthesize(
            text=translated_text,
            language=target_language,
            output_path=output_path,
        )

        return {
            "source_language": source_language,
            "confidence": prediction["confidence"],
            "probabilities": prediction["probabilities"],
            "transcript": transcript,
            "translated_text": translated_text,
            "output_audio_path": saved_audio_path,
        }
