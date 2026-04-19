from src.model.inference import LanguageClassifier
from src.pipeline.asr import WhisperSpeechRecognizer


class LanguageToTextPipeline:
    def __init__(self, model_path, whisper_model="base"):
        self.classifier = LanguageClassifier(model_path=model_path)
        self.recognizer = WhisperSpeechRecognizer(model_name=whisper_model)

    def run(self, audio_path):
        prediction = self.classifier.predict(audio_path)
        detected_language = prediction["language"]

        transcript = self.recognizer.transcribe(
            audio_path,
            language_code=detected_language,
        )

        return {
            "detected_language": detected_language,
            "confidence": prediction["confidence"],
            "probabilities": prediction["probabilities"],
            "transcript": transcript,
        }
