from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_ANON_KEY')

print("🔍 Starting Supabase client connection test...")

try:
    supabase = create_client(url, key)
    response = supabase.table('test_table').select('*').execute()
    print("✅ Supabase connected successfully! Sample data:", response.data)
except Exception as e:
    print("❌ Supabase connection error:", e)
