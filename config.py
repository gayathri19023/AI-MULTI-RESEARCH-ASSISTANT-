"""Application configuration loaded from environment variables."""
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
DATABASE_URL = f"sqlite:///{BASE_DIR / 'data' / 'research.db'}"
REPORTS_DIR = BASE_DIR / "reports"
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY", "")
DEFAULT_DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"
for directory in (BASE_DIR / "data", REPORTS_DIR):
    directory.mkdir(exist_ok=True)
