import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import APP_NAME
from src.database.db import DatabaseManager
from src.rag.pdf_loader import PDFLoader
from src.rag.document_processor import DocumentProcessor

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

                    analysis = DocumentProcessor.analyze(
                        pdf_info["text"]
                    )

                    st.markdown("---")
                    st.subheader("Document Analysis")

                    col1, col2, col3 = st.columns(3)

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

                    st.subheader(
                        "Document Preview"
                    )

                    st.text_area(
                        "Extracted Text",
                        analysis["preview"],
                        height=350
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

elif page == "🎫 Tickets":

    st.title("Support Tickets")

    st.info(
        "Ticket Management Module Coming Soon"
    )

# ---------------------------------------
# Analytics
# ---------------------------------------

elif page == "📊 Analytics":

    st.title("Analytics Dashboard")

    st.info(
        "Analytics Dashboard Coming Soon"
    )

# ---------------------------------------
# Feedback
# ---------------------------------------

elif page == "⭐ Feedback":

    st.title("Feedback Center")

    st.info(
        "Feedback Module Coming Soon"
    )