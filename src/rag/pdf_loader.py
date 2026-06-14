from pypdf import PdfReader


class PDFLoader:

    @staticmethod
    def extract_text(pdf_path):
        try:
            reader = PdfReader(pdf_path)
            pages = len(reader.pages)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return {
                "success": True,
                "pages": pages,
                "text": text
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
