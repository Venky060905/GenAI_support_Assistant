from pathlib import Path

from src.config.settings import PDF_DIR
from src.utils.logger import get_logger

logger = get_logger()


def save_uploaded_file(uploaded_file):
    current_dir = Path.cwd()
    logger.info("Starting file save for uploaded PDF")
    logger.info(f"Current Working Directory: {current_dir}")
    logger.info(f"Resolved PDF_DIR: {PDF_DIR}")

    PDF_DIR.mkdir(parents=True, exist_ok=True)

    file_path = PDF_DIR / uploaded_file.name
    logger.info(f"Saving uploaded file to: {file_path}")

    try:
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    except Exception as exc:
        logger.exception("Failed to save uploaded file")
        raise

    file_exists = file_path.exists()
    logger.info(f"File exists after save: {file_exists}")

    return file_path, file_exists
