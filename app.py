import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.config.settings import APP_NAME
from src.database.db import DatabaseManager

# Initialize Database
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
            saved_path, file_exists = save_uploaded_file(uploaded_file)

            if file_exists:
                db.add_document(uploaded_file.name)
                st.success(f"{uploaded_file.name} uploaded successfully.")
            else:
                st.error("File upload completed but the file is missing on disk.")

        except Exception as exc:
            st.error(f"Failed to save uploaded PDF: {exc}")
            st.warning("Please check server logs for more details.")

    st.markdown("---")

    st.subheader(
        "Uploaded Documents"
    )

    documents = db.get_documents()

    if documents:

        for doc in documents:
            st.write(f"📄 {doc[1]}")

    else:
        st.info("No documents uploaded yet.")

# ---------------------------------------
# Tickets
# ---------------------------------------

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