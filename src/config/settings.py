from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
FAISS_DIR = DATA_DIR / "faiss_index"

DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "support.db"

LOG_DIR = BASE_DIR / "logs"
LOG_FILE = BASE_DIR / "app.log"

APP_NAME = "Generative AI Customer Support Assistant"
VERSION = "1.0.0"

MODEL_NAME = "llama3"

SUPPORTED_FILE_TYPES = ["pdf"]
MAX_UPLOAD_SIZE_MB = 25
