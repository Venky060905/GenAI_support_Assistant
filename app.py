import logging
import sys
import traceback
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import APP_NAME
from src.database.db import DatabaseManager
from src.rag.document_processor import DocumentProcessor
from src.rag.pdf_loader import PDFLoader
from src.rag.text_chunker import TextChunker

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# ---------------------------------------
# Initialize Database
# ---------------------------------------

db = DatabaseManager()

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------
# Sidebar
# ---------------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Home",
        "💬 Chat Assistant",
        "📄 Upload Documents",
        "🎫 Tickets",
        "📊 Analytics",
        "⭐ Feedback"
    ]
)

# ---------------------------------------
# Home
# ---------------------------------------

if page == "🏠 Home":

    st.title(APP_NAME)

    st.markdown("---")

    st.subheader(
        "Enterprise Generative AI Customer Support Assistant"
    )

    docs_count = len(db.get_documents())

    col1, col2, col3 = st.columns(3)

    col1.metric("Documents", docs_count)
    col2.metric("Tickets", 0)
    col3.metric("Feedback", 0)

# ---------------------------------------
# Chat Assistant
# ---------------------------------------

elif page == "💬 Chat Assistant":

    st.title("AI Chat Assistant")

    st.info(
        "RAG Chatbot will be integrated in upcoming sprint."
    )

# ---------------------------------------
# Upload Documents
# ---------------------------------------

elif page == "📄 Upload Documents":

    st.title("Upload Knowledge Base")

    uploaded_file = st.file_uploader(
        "Choose PDF File",
        type=["pdf"]
    )

    if uploaded_file:

        from src.utils.file_handler import save_uploaded_file

        try:

            saved_path, file_exists = save_uploaded_file(
                uploaded_file
            )

            if file_exists:

                db.add_document(
                    uploaded_file.name
                )

                st.success(
                    f"{uploaded_file.name} uploaded successfully."
                )

                # --------------------------------
                # PDF EXTRACTION
                # --------------------------------

                pdf_info = PDFLoader.extract_text(
                    saved_path
                )

                if pdf_info["success"]:

                    # Analyze document
                    analysis = DocumentProcessor.analyze(
                        pdf_info["text"]
                    )

                    # Create chunks
                    chunks = []
                    try:
                        chunks = TextChunker.create_chunks(
                            pdf_info["text"]
                        )
                        logger.debug(
                            "Text length=%s chunk_count=%s",
                            len(pdf_info["text"]),
                            len(chunks)
                        )
                    except Exception as exc:
                        logger.exception("Chunk generation failed")
                        st.error(
                            f"Chunk generation failed: {exc}"
                        )
                        st.text(
                            traceback.format_exc()
                        )

                    st.write("Text Length:", len(pdf_info["text"]))
                    st.write("Chunk Count:", len(chunks))
                    st.write(chunks[:2])

                    st.markdown("---")
                    st.subheader("Document Analysis")

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric(
                        "Pages",
                        pdf_info["pages"]
                    )

                    col2.metric(
                        "Words",
                        analysis["words"]
                    )

                    col3.metric(
                        "Characters",
                        analysis["characters"]
                    )

                    col4.metric(
                        "Chunks",
                        len(chunks)
                    )

                    # Preview extracted text
                    st.subheader(
                        "Document Preview"
                    )

                    st.text_area(
                        "Extracted Text",
                        analysis["preview"],
                        height=250
                    )

                    # Preview chunks
                    st.subheader(
                        "Chunk Preview"
                    )

                    if chunks:
                        for index, chunk in enumerate(chunks[:3], start=1):
                            st.text_area(
                                f"Chunk {index}",
                                chunk,
                                height=200
                            )
                    else:
                        st.info(
                            "No chunks were generated from this document. "
                            "If the PDF text is very short, the chunk size may be larger than the text length."
                        )

                    st.success(
                        f"Successfully created {len(chunks)} chunks."
                    )

                else:

                    st.error(
                        f"PDF Extraction Error: {pdf_info['error']}"
                    )

            else:

                st.error(
                    "File upload failed."
                )

        except Exception as exc:

            st.error(
                f"Failed to process PDF: {exc}"
            )

    st.markdown("---")

    st.subheader(
        "Uploaded Documents"
    )

    documents = db.get_documents()

    if documents:

        for doc in documents:

            st.write(
                f"📄 {doc[1]}"
            )

    else:

        st.info(
            "No documents uploaded yet."
        )

# ---------------------------------------
# Feedback
# ---------------------------------------

elif page == "⭐ Feedback":

    st.title("Feedback Center")

    st.info(
        "Feedback Module Coming Soon"
    )