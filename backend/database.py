from supabase import create_client, Client
import os

def get_supabase() -> Client:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Missing Supabase environment variables!")
        return None

    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print("❌ Failed to connect to Supabase:", e)
        return None
