try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
    except ImportError:
        from langchain_text_splitters.character import RecursiveCharacterTextSplitter


class TextChunker:

    @staticmethod
    def create_chunks(text, chunk_size=500, chunk_overlap=100):
        if not text:
            return []

        text_length = len(text)
        if text_length <= chunk_size:
            chunk_size = max(100, text_length // 2)

        chunk_overlap = min(chunk_overlap, chunk_size // 2)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

        chunks = splitter.split_text(text)

        if not chunks and text_length > 0:
            return [text]

        return chunks
