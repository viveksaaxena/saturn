

from supabase import create_client, Client
import os
from dotenv import load_dotenv
from pathlib import Path

print("🔥 database.py STARTED")


# Get the directory of this file
BASE_DIR = Path(__file__).resolve().parent

# Load .env file explicitly
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Validation
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL and SUPABASE_KEY must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
print("✅ Supabase connected successfully!")
