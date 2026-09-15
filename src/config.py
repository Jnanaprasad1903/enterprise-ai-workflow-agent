import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project (d:/Office_agent)
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file from the project root if it exists
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    # Also load from system environment
    load_dotenv()

# Data & Persistence Paths
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "docs"
DATABASE_PATH = DATA_DIR / os.getenv("DATABASE_FILE", "enterprise.db")
CHROMA_PERSIST_DIR = DATA_DIR / os.getenv("CHROMA_DIR", "chroma_db")

# Ensure required data directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

# Google Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Server Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
