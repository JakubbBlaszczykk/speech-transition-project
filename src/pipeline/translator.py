from deep_translator import GoogleTranslator


class TranslatorBackend:
    def translate(self, text, source_language, target_language):
        translator = GoogleTranslator(source=source_language, target=target_language)
        return translator.translate(text)
