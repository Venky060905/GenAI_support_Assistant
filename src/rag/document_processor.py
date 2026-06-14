class DocumentProcessor:

    @staticmethod
    def analyze(text):

        words = len(text.split())

        characters = len(text)

        preview = text[:1000]

        return {
            "words": words,
            "characters": characters,
            "preview": preview
        }