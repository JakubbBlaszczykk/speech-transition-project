from gtts import gTTS


class TTSBackend:
    def synthesize(self, text, language, output_path):
        tts = gTTS(text=text, lang=language)
        tts.save(output_path)
        return output_path
